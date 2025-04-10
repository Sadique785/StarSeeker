import json
import os
import time
import logging
from django.core.management.base import BaseCommand
from artists.models import Artist, NewArtist
import musicbrainzngs
from django.db import transaction
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='artist_import.log'
)
logger = logging.getLogger(__name__)

def save_checkpoint(offset, artists_added, checkpoint_file):
    """Save current progress to a checkpoint file"""
    checkpoint = {
        'offset': offset,
        'artists_added': artists_added,
        'timestamp': time.time()
    }
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint, f)

def load_checkpoint(checkpoint_file):
    """Load progress from a checkpoint file"""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            return json.load(f)
    return None

class Command(BaseCommand):
    help = 'Fetch artists from MusicBrainz and store them in the database - Fast version'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=100000, help='Number of artists to fetch')
        parser.add_argument('--batch-size', type=int, default=100, help='Batch size for each API request')
        parser.add_argument('--start-offset', type=int, default=0, help='Starting offset for API pagination')
        parser.add_argument('--end-offset', type=int, default=None, help='Ending offset for API pagination')
        parser.add_argument('--process-id', type=int, default=1, help='Process ID for parallel imports')
        parser.add_argument('--rate-limit', type=float, default=1.0, help='Time between API requests in seconds')

    def handle(self, *args, **options):
        limit = options['limit']
        batch_size = options['batch_size']
        process_id = options['process_id']
        rate_limit = options['rate_limit']
        
        # Use process-specific checkpoint file
        checkpoint_file = f'artist_import_checkpoint_{process_id}.json'
        
        # Load checkpoint
        checkpoint = load_checkpoint(checkpoint_file)
        if checkpoint and options['start_offset'] == 0:
            offset = checkpoint['offset']
            artists_added = checkpoint['artists_added']
            self.stdout.write(f"Process {process_id}: Resuming from checkpoint: offset={offset}, artists_added={artists_added}")
        else:
            offset = options['start_offset']
            artists_added = 0
        
        # Set end offset if provided
        end_offset = options['end_offset'] or offset + limit
        
        musicbrainzngs.set_useragent(
            "StarSeeker", 
            "0.1", 
            "vssadiquedfd@gmail.com"
        )

        progress_bar = tqdm(total=min(limit, end_offset - offset), 
                           desc=f"Process {process_id}: Fetching artists", 
                           position=process_id-1)
        
        # Dictionary to track processed artists to avoid duplicates
        processed_artists = {}

        while artists_added < limit and offset < end_offset:
            try:
                # Fetch a batch of artists - using a wildcard search to get all artists
                self.stdout.write(f"Process {process_id}: Fetching artists (offset: {offset}, batch: {batch_size})")
                
                # Using a wildcard search term to get all artists
                start_time = time.time()
                results = musicbrainzngs.search_artists("*", limit=batch_size, offset=offset)
                request_time = time.time() - start_time
                
                # Adjust rate limiting based on request time
                sleep_time = max(0, rate_limit - request_time)
                
                if 'artist-list' not in results or not results['artist-list']:
                    self.stdout.write(self.style.WARNING(f"Process {process_id}: No artists found. API response: {results}"))
                    break

                artists_batch = []
                for artist_data in results['artist-list']:
                    # Skip if we already have this artist
                    artist_id = artist_data.get('id')
                    if not artist_id or artist_id in processed_artists:
                        continue
                    
                    processed_artists[artist_id] = True
                    
                    # Quick processing - skip the extra API calls
                    artist = self._fast_process_artist(artist_data)
                    if artist:
                        artists_batch.append(artist)
                
                # Bulk create artists in database
                with transaction.atomic():
                    created = NewArtist.objects.bulk_create(
                        artists_batch, 
                        ignore_conflicts=True
                    )
                
                batch_added = len(artists_batch)
                artists_added += batch_added
                progress_bar.update(batch_added)
                
                # Save checkpoint after successful batch
                save_checkpoint(offset, artists_added, checkpoint_file)
                
                # Sleep only the necessary amount based on API rate limit
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
                offset += batch_size
                
                # Log progress
                logger.info(f"Process {process_id}: Added {batch_added} artists. Total: {artists_added}/{limit}")
                
                # Print progress every 10 batches
                if (offset // batch_size) % 10 == 0:
                    self.stdout.write(f"Process {process_id}: Added {batch_added} artists. Total: {artists_added}/{limit}")
                
                if artists_added >= limit or offset >= end_offset:
                    break

            except Exception as e:
                logger.error(f"Process {process_id}: Error fetching artists: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Process {process_id}: Error: {str(e)}"))
                time.sleep(2)  # Short wait on error
        
        progress_bar.close()
        self.stdout.write(self.style.SUCCESS(f"Process {process_id}: Successfully imported {artists_added} artists"))
    
    def _fast_process_artist(self, artist_data):
        """Process artist data from MusicBrainz quickly - skip extra API calls"""
        try:
            name = artist_data.get('name', '')
            
            # Skip artists with no name
            if not name:
                return None
            
            # Get artist details
            artist_id = artist_data.get('id')
            
            # Use simple placeholder for genre - we'll update this later
            genre = "Unknown"
                 
            # Get location
            location = artist_data.get('country', 'Unknown')
            if not location or location == "":
                location = "Unknown"
            
            # Use a predictable placeholder image - we'll update these later
            profile_picture = f"https://picsum.photos/seed/{artist_id}/400/400"
            
            # Create new Artist instance (not saved to DB yet)
            return NewArtist(
                name=name[:255],  # Truncate to fit model field
                genre=genre[:255],
                location=location[:255],
                profile_picture=profile_picture
            )
        
        except Exception as e:
            logger.error(f"Error processing artist {artist_data.get('name', 'Unknown')}: {str(e)}")
            return None