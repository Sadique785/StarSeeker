import os
from dotenv import load_dotenv
import time
import base64
import logging
import requests
import concurrent.futures
import json
from typing import Dict, List, Optional
import django
from django.db.models import Q
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("spotify_popularity_fetcher.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("spotify_popularity_fetcher")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'star_seeker.settings')  
django.setup()

load_dotenv()

from artists.models import Artist 

class SpotifyPopularityFetcher:
    """Class to fetch artist popularity from Spotify API and update database."""
    
    def __init__(self, client_id: str, client_secret: str, batch_size: int = 100, checkpoint_file: str = "spotify_popularity_checkpoint.json"):
        """
        Initialize the fetcher with Spotify API credentials.
        
        Args:
            client_id: Spotify API client ID
            client_secret: Spotify API client secret
            batch_size: Number of artists to process in each batch
            checkpoint_file: File to store checkpoint data for resuming
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
        self.checkpoint_file = checkpoint_file
        
        # Stats tracking
        self.stats = {
            'total': 0,
            'updated': 0,
            'not_found': 0,
            'errors': 0,
            'skipped': 0,
        }
        
        # Load checkpoint if exists
        self.last_processed_id = self.load_checkpoint()
    
    def save_checkpoint(self, artist_id: int) -> None:
        """
        Save the last processed artist ID to the checkpoint file.
        
        Args:
            artist_id: ID of the last processed artist
        """
        checkpoint_data = {
            'last_processed_id': artist_id,
            'timestamp': time.time(),
            'stats': self.stats
        }
        
        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint_data, f)
            logger.info(f"Checkpoint saved: Last processed artist ID {artist_id}")
        except Exception as e:
            logger.error(f"Error saving checkpoint: {str(e)}")
    
    def load_checkpoint(self) -> Optional[int]:
        """
        Load the last processed artist ID from the checkpoint file.
        
        Returns:
            Last processed artist ID if checkpoint exists, None otherwise
        """
        if not os.path.exists(self.checkpoint_file):
            logger.info("No checkpoint file found, starting from the beginning")
            return None
        
        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
            
            last_id = checkpoint_data.get('last_processed_id')
            saved_stats = checkpoint_data.get('stats', {})
            
            # Restore stats from checkpoint
            if saved_stats:
                self.stats = saved_stats
                logger.info(f"Restored stats from checkpoint: {self.stats}")
            
            logger.info(f"Resuming from checkpoint: Last processed artist ID {last_id}")
            return last_id
        except Exception as e:
            logger.error(f"Error loading checkpoint: {str(e)}. Starting from the beginning.")
            return None
    
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
    
    def process_artist(self, artist: Artist) -> bool:
        """
        Process a single artist to update popularity.
        
        Args:
            artist: Artist model instance to update
            
        Returns:
            True if updated successfully, False otherwise
        """
        # Skip if artist already has a non-zero popularity
        if artist.popularity > 0:
            self.stats['skipped'] += 1
            return False
        
        artist_data = self.search_artist(artist.name)
        if not artist_data:
            self.stats['not_found'] += 1
            return False
        
        # Extract popularity from artist data
        popularity = artist_data.get('popularity', 0)
        
        # Update the artist model
        try:
            artist.popularity = popularity
            artist.save(update_fields=['popularity'])
            self.stats['updated'] += 1
            
            # Save checkpoint after processing each artist
            self.save_checkpoint(artist.id)
            return True
        except Exception as e:
            logger.error(f"Error saving popularity for artist {artist.name}: {str(e)}")
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
                # Still save checkpoint on error to mark this artist as processed
                self.save_checkpoint(artist.id)
    
    def process_all(self, max_workers: int = 4) -> Dict:
        """
        Process all artists in batches using multiple workers.
        
        Args:
            max_workers: Number of parallel workers
            
        Returns:
            Statistics dictionary
        """
        # Build the base query - only artists with zero popularity
        base_query = Artist.objects.filter(popularity=0)
        
        # If we have a checkpoint, add condition to only process artists with ID > last_processed_id
        if self.last_processed_id is not None:
            base_query = base_query.filter(id__gt=self.last_processed_id)
        
        total_artists = base_query.count()
        
        logger.info(f"Found {total_artists} artists to process for popularity")
        self.stats['total'] = total_artists
        
        # Process in batches
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            offset = 0
            while offset < total_artists:
                artists_batch = list(base_query.order_by('id')[offset:offset+self.batch_size])
                
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
    """Main function to run the popularity fetcher."""
    # Get Spotify API credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        logger.error("Spotify API credentials not found in environment variables")
        print("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables")
        return
    
    fetcher = SpotifyPopularityFetcher(
        client_id=client_id,
        client_secret=client_secret,
        batch_size=50,  # Process 50 artists at a time
        checkpoint_file="spotify_popularity_checkpoint.json"  # Separate checkpoint file for popularity
    )
    
    try:
        start_time = time.time()
        stats = fetcher.process_all(max_workers=4)  # Use 4 parallel workers
        end_time = time.time()
        
        print("\n--- Processing complete ---")
        print(f"Total artists: {stats['total']}")
        print(f"Updated with popularity: {stats['updated']}")
        print(f"Not found: {stats['not_found']}")
        print(f"Errors: {stats['errors']}")
        print(f"Skipped: {stats['skipped']}")
        print(f"Time taken: {(end_time - start_time) / 60:.2f} minutes")
    except KeyboardInterrupt:
        print("\n--- Processing interrupted by user ---")
        print("You can resume processing by running the script again")
        print("The script will continue from the last saved checkpoint")


if __name__ == '__main__':
    main()