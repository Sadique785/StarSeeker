import logging
import time
from typing import List, Dict, Optional, Tuple
from django.conf import settings
from .models import Artist
from .spotify_client import SpotifyClient

logger = logging.getLogger(__name__)

class ArtistProfileUpdater:
    """
    Utility for updating artist profile pictures from Spotify
    """
    def __init__(self):
        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.spotify = SpotifyClient(client_id, client_secret)
        
        # Configure rate limiting (Spotify allows ~30 requests per second)
        self.requests_per_second = 20  # Conservative limit
        self.last_request_time = 0
    
    def _rate_limit(self) -> None:
        """
        Simple rate limiting to avoid hitting Spotify API limits
        """
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        # If we're making requests too quickly, sleep to stay under the limit
        min_interval = 1.0 / self.requests_per_second
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self.last_request_time = time.time()
    
    def get_artist_profile_picture(self, artist_name: str) -> Optional[str]:
        """
        Get the profile picture URL for an artist by name
        
        Returns:
            URL of the largest available profile picture, or None if not found
        """
        self._rate_limit()
        
        try:
            artist_data = self.spotify.get_best_artist_match(artist_name)
            
            if not artist_data:
                return None
            
            # Spotify provides multiple image sizes - get the largest one
            images = artist_data.get("images", [])
            if not images:
                logger.info(f"No profile picture found for artist '{artist_name}'")
                return None
            
            # Sort by size (largest first) and return the URL
            largest_image = sorted(images, key=lambda img: img.get("width", 0) or 0, reverse=True)[0]
            return largest_image.get("url")
            
        except Exception as e:
            logger.error(f"Error getting profile picture for '{artist_name}': {str(e)}")
            return None
        
    def update_all_artists(self, batch_size: int = 100) -> Dict[str, int]:
            """
            Update all artists without profile pictures
            
            Args:
                batch_size: Number of artists to process in each batch
                
            Returns:
                Dictionary with statistics about the operation
            """
            stats = {
                "total": 0,
                "updated": 0,
                "failed": 0,
                "skipped": 0
            }
            
            # Get all artists without a profile picture
            artists_to_update = Artist.objects.filter(profile_picture__isnull=True)
            stats["total"] = artists_to_update.count()
            
            logger.info(f"Starting update for {stats['total']} artists without profile pictures")
            
            # Process in batches to avoid loading too many records at once
            offset = 0
            while True:
                batch = artists_to_update[offset:offset+batch_size]
                if not batch:
                    break
                    
                for artist in batch:
                    try:
                        if self.update_artist(artist):
                            stats["updated"] += 1
                        else:
                            stats["failed"] += 1
                    except Exception as e:
                        logger.error(f"Error updating artist '{artist.name}': {str(e)}")
                        stats["failed"] += 1
                
                offset += batch_size
                logger.info(f"Processed {offset} artists so far ({stats['updated']} updated, {stats['failed']} failed)")
            
            # Log final statistics
            logger.info(f"Artist profile picture update complete: {stats['updated']} updated, {stats['failed']} failed, {stats['skipped']} skipped")
            
            return stats