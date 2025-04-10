import json
import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from artists.models import Artist
import musicbrainzngs
from django.db import transaction
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='artist_genre_update.log'
)
logger = logging.getLogger(__name__)

# Set up MusicBrainz once
musicbrainzngs.set_useragent(
    "StarSeeker", 
    "0.1", 
    "vssadiquedfd@gmail.com"
)

def update_artist_genre(artist):
    """Update genre for a single artist"""
    try:
        # Search for artist in MusicBrainz to get MBID
        results = musicbrainzngs.search_artists(artist.name, limit=1)
        if 'artist-list' not in results or not results['artist-list']:
            logger.warning(f"No MusicBrainz artist found for {artist.name}")
            return None
        
        mbid = results['artist-list'][0].get('id')
        if not mbid:
            return None
        
        # Get genre info
        try:
            artist_info = musicbrainzngs.get_artist_by_id(mbid, includes=["genres"])
            genres = artist_info.get('artist', {}).get('genre-list', [])
            
            if genres:
                # Extract genre names and join with commas
                genre = ", ".join([g.get('name', '') for g in genres if 'name' in g])
                return genre[:255]  # Truncate to fit field
            else:
                return "Unknown"
        except Exception as e:
            logger.warning(f"Error fetching genres for {artist.name}: {str(e)}")
            return None
        
    except Exception as e:
        logger.error(f"Error updating artist {artist.name}: {str(e)}")
        return None

def process_artist_batch(artist_batch, rate_limit=1.0):
    """Process a batch of artists and return updates"""
    results = []
    
    for artist in artist_batch:
        start_time = time.time()
        genre = update_artist_genre(artist)
        
        if genre is not None:
            results.append((artist.id, genre))
        
        # Apply rate limiting
        request_time = time.time() - start_time
        sleep_time = max(0, rate_limit - request_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
    
    return results

class Command(BaseCommand):
    help = 'Update genre information for existing artists using multi-threading'

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=100, help='Number of artists to process in a batch')
        parser.add_argument('--max-workers', type=int, default=4, help='Maximum number of worker threads')
        parser.add_argument('--rate-limit', type=float, default=1.0, help='Time between API requests in seconds per thread')
        parser.add_argument('--chunk-size', type=int, default=1000, help='Number of artists to load at once from database')

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        max_workers = options['max_workers']
        rate_limit = options['rate_limit']
        chunk_size = options['chunk_size']
        
        # Create checkpoint file
        checkpoint_file = 'artist_genre_update_checkpoint.json'
        checkpoint = self._load_checkpoint(checkpoint_file)
        
        last_artist_id = checkpoint.get('last_artist_id', 0) if checkpoint else 0
        artists_updated = checkpoint.get('artists_updated', 0) if checkpoint else 0
        
        self.stdout.write(f"Starting genre update with {max_workers} workers")
        if last_artist_id > 0:
            self.stdout.write(f"Resuming from artist ID {last_artist_id}, already updated {artists_updated} artists")
        
        # Process in chunks to avoid loading entire dataset into memory
        total_remaining = Artist.objects.filter(id__gt=last_artist_id, genre="Unknown").count()
        self.stdout.write(f"Found {total_remaining} artists to update")
        
        with tqdm(total=total_remaining, desc="Updating artist genres") as progress_bar:
            while True:
                # Get next chunk of artists
                artists_chunk = list(Artist.objects.filter(
                    id__gt=last_artist_id, 
                    genre="Unknown"
                ).order_by('id')[:chunk_size])
                
                if not artists_chunk:
                    break  # No more artists to process
                
                # Process artists in parallel batches
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Split chunk into batches
                    batches = [artists_chunk[i:i+batch_size] for i in range(0, len(artists_chunk), batch_size)]
                    
                    # Submit all batches to the executor
                    future_to_batch = {
                        executor.submit(process_artist_batch, batch, rate_limit): batch 
                        for batch in batches
                    }
                    
                    # Collect results as they complete
                    all_updates = []
                    for future in tqdm(
                        future_to_batch, 
                        total=len(future_to_batch), 
                        desc="Processing batches",
                        leave=False
                    ):
                        batch_results = future.result()
                        all_updates.extend(batch_results)
                
                # Apply updates in bulk using a more efficient approach
                if all_updates:
                    with transaction.atomic():
                        # Use Django's bulk_update with a dictionary for efficiency
                        update_dict = {artist_id: genre for artist_id, genre in all_updates}
                        
                        # Get artists to update
                        artists_to_update = list(Artist.objects.filter(id__in=update_dict.keys()))
                        
                        # Update each artist's genre
                        for artist in artists_to_update:
                            artist.genre = update_dict[artist.id]
                        
                        # Bulk update
                        if artists_to_update:
                            Artist.objects.bulk_update(artists_to_update, ['genre'])
                    
                    # Update checkpoint
                    last_artist_id = artists_chunk[-1].id
                    artists_updated += len(all_updates)
                    self._save_checkpoint(last_artist_id, artists_updated, checkpoint_file)
                    
                    # Update progress
                    progress_bar.update(len(artists_chunk))
                    self.stdout.write(f"Updated {artists_updated} artists so far")
        
        self.stdout.write(self.style.SUCCESS(f"Successfully updated {artists_updated} artists"))

    def _save_checkpoint(self, artist_id, artists_updated, checkpoint_file):
        """Save current progress to a checkpoint file"""
        checkpoint = {
            'last_artist_id': artist_id,
            'artists_updated': artists_updated,
            'timestamp': time.time()
        }
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)

    def _load_checkpoint(self, checkpoint_file):
        """Load progress from a checkpoint file"""
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                return json.load(f)
        return None