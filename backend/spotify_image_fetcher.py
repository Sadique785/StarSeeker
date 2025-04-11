import os
from dotenv import load_dotenv
import time
import base64
import logging
import requests
import concurrent.futures
from typing import Dict, List, Optional, Tuple
import django
from django.db import transaction
from django.db.models import Q
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("spotify_image_fetcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("spotify_image_fetcher")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'star_seeker.settings')  
django.setup()

load_dotenv()

from artists.models import Artist 

class SpotifyImageFetcher:
    """Class to fetch artist images from Spotify API and update database."""
    
    def __init__(self, client_id: str, client_secret: str, batch_size: int = 100):
        """
        Initialize the fetcher with Spotify API credentials.
        
        Args:
            client_id: Spotify API client ID
            client_secret: Spotify API client secret
            batch_size: Number of artists to process in each batch
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = 0
        self.batch_size = batch_size
        self.session = requests.Session()
        self.default_headers = {
            'Content-Type': 'application/json',
        }
        
        # Stats tracking
        self.stats = {
            'total': 0,
            'updated': 0,
            'not_found': 0,
            'errors': 0,
            'skipped': 0,
        }
    
    def authenticate(self) -> None:
        """Obtain an access token from Spotify API."""
        if self.access_token and time.time() < self.token_expiry:
            return  # Token is still valid
        
        logger.info("Getting new Spotify access token")
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            'Authorization': f"Basic {auth_base64}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
        }
        
        try:
            response = self.session.post(url, headers=headers, data=data)
            response.raise_for_status()
            json_response = response.json()
            
            self.access_token = json_response['access_token']
            # Set expiry to 1 minute before actual expiry to be safe
            self.token_expiry = time.time() + json_response['expires_in'] - 60
            self.default_headers['Authorization'] = f"Bearer {self.access_token}"
            logger.info("Successfully authenticated with Spotify API")
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise
            
    def search_artist(self, artist_name: str) -> Optional[Dict]:
        """
        Search for an artist on Spotify.
        
        Args:
            artist_name: Name of the artist to search for
            
        Returns:
            Artist data if found, None otherwise
        """
        try:
            self.authenticate()  # Ensure token is valid
            
            url = "https://api.spotify.com/v1/search"
            params = {
                'q': artist_name,
                'type': 'artist',
                'limit': 1  # Get only the top match
            }
            
            response = self.session.get(url, headers=self.default_headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['artists']['items']:
                return data['artists']['items'][0]
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                retry_after = int(e.response.headers.get('Retry-After', 1))
                logger.warning(f"Rate limited. Waiting for {retry_after} seconds.")
                time.sleep(retry_after)
                return self.search_artist(artist_name)  # Retry after waiting
            else:
                logger.error(f"HTTP error searching for '{artist_name}': {str(e)}")
                return None
        except Exception as e:
            logger.error(f"Error searching for '{artist_name}': {str(e)}")
            return None
    
    def get_best_image(self, images: List[Dict]) -> Optional[str]:
        """
        Get the best image URL from a list of Spotify image objects.
        
        Args:
            images: List of image objects from Spotify API
            
        Returns:
            URL of the best image (medium size preferred) or None if no images
        """
        if not images:
            return None
            
        # Sort images by size (width), getting medium-sized images ideally
        # Spotify usually provides images in 3 sizes, we prefer the middle one
        if len(images) >= 3:
            sorted_images = sorted(images, key=lambda x: x.get('width', 0))
            return sorted_images[len(images) // 2]['url']  # Get middle-sized image
        
        # If there are fewer images, get the largest one
        return max(images, key=lambda x: x.get('width', 0)).get('url')
    
    def process_artist(self, artist: Artist) -> bool:
        """
        Process a single artist.
        
        Args:
            artist: Artist model instance to update
            
        Returns:
            True if updated successfully, False otherwise
        """
        # Skip if artist already has a valid profile picture
        if artist.profile_picture and not artist.profile_picture.startswith('https://picsum.photos/'):
            self.stats['skipped'] += 1
            return False
        
        artist_data = self.search_artist(artist.name)
        if not artist_data:
            self.stats['not_found'] += 1
            return False
        
        image_url = self.get_best_image(artist_data.get('images', []))
        if not image_url:
            self.stats['not_found'] += 1
            return False
            
        # Update the artist model
        try:
            artist.profile_picture = image_url
            artist.save(update_fields=['profile_picture'])
            self.stats['updated'] += 1
            return True
        except Exception as e:
            logger.error(f"Error saving artist {artist.name}: {str(e)}")
            self.stats['errors'] += 1
            return False
    
    def process_batch(self, artists: List[Artist]) -> None:
        """
        Process a batch of artists.
        
        Args:
            artists: List of Artist model instances to process
        """
        for artist in tqdm(artists, desc="Processing artists batch"):
            try:
                self.process_artist(artist)
            except Exception as e:
                logger.error(f"Error processing artist {artist.name}: {str(e)}")
                self.stats['errors'] += 1
    
    def process_all(self, max_workers: int = 4) -> Dict:
        """
        Process all artists in batches using multiple workers.
        
        Args:
            max_workers: Number of parallel workers
            
        Returns:
            Statistics dictionary
        """
        total_artists = Artist.objects.filter(
            Q(profile_picture__isnull=True) | 
            Q(profile_picture__startswith='https://picsum.photos/')
        ).count()
        
        logger.info(f"Found {total_artists} artists to process")
        self.stats['total'] = total_artists
        
        # Process in batches
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            offset = 0
            while offset < total_artists:
                artists_batch = list(Artist.objects.filter(
                    Q(profile_picture__isnull=True) | 
                    Q(profile_picture__startswith='https://picsum.photos/')
                ).order_by('id')[offset:offset+self.batch_size])
                
                if not artists_batch:
                    break
                    
                future = executor.submit(self.process_batch, artists_batch)
                futures.append(future)
                offset += self.batch_size
                
                # Add small delay to avoid overwhelming the database
                time.sleep(0.1)
            
            # Wait for all futures to complete
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Completing batches"):
                try:
                    future.result()  # Get result to catch any exceptions
                except Exception as e:
                    logger.error(f"Batch processing error: {str(e)}")
                    self.stats['errors'] += 1
        
        logger.info(f"Processed {total_artists} artists")
        logger.info(f"Stats: {self.stats}")
        return self.stats


def main():
    """Main function to run the image fetcher."""
    # Replace these with your actual Spotify API credentials
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        logger.error("Spotify API credentials not found in environment variables")
        print("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables")
        return
    
    fetcher = SpotifyImageFetcher(
        client_id=client_id,
        client_secret=client_secret,
        batch_size=50  # Process 50 artists at a time
    )
    
    start_time = time.time()
    stats = fetcher.process_all(max_workers=4)  # Use 4 parallel workers
    end_time = time.time()
    
    print("\n--- Processing complete ---")
    print(f"Total artists: {stats['total']}")
    print(f"Updated: {stats['updated']}")
    print(f"Not found: {stats['not_found']}")
    print(f"Errors: {stats['errors']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Time taken: {(end_time - start_time) / 60:.2f} minutes")


if __name__ == '__main__':
    main()