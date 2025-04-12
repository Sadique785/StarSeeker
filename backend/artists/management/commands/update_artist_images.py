from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from ...spotify_updater import ArtistProfileUpdater  

class Command(BaseCommand):
    help = 'Update artist profile pictures from Spotify API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Number of artists to process in each batch'
        )
        parser.add_argument(
            '--artist-id',
            type=int,
            help='Update a specific artist by ID'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit the number of artists to update'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if artists already have profile pictures'
        )

    def handle(self, *args, **options):
        updater = ArtistProfileUpdater()
        
        # Handle single artist update
        if options['artist_id']:
            from ...models import Artist  # Adjust import path as needed
            try:
                artist = Artist.objects.get(id=options['artist_id'])
                self.stdout.write(f"Updating artist: {artist.name}")
                
                if options['force'] or not artist.profile_picture:
                    success = updater.update_artist(artist)
                    if success:
                        self.stdout.write(self.style.SUCCESS(f"Successfully updated profile picture for '{artist.name}'"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Could not find profile picture for '{artist.name}'"))
                else:
                    self.stdout.write(self.style.WARNING(f"Artist '{artist.name}' already has a profile picture. Use --force to update anyway."))
                
                return
            except Artist.DoesNotExist:
                raise CommandError(f"Artist with ID {options['artist_id']} not found")
        
        # Handle batch update for all artists
        batch_size = options['batch_size']
        limit = options['limit']
        
        self.stdout.write(f"Starting batch update with batch size: {batch_size}")
        self.stdout.write(f"Limit: {'unlimited' if limit is None else limit}")
        
        if options['force']:
            self.stdout.write(self.style.WARNING("Force mode enabled - will update all artists, even those with existing images"))
            # In this case, create a custom method in the updater to handle this
            stats = updater.update_artists_force(batch_size=batch_size, limit=limit)
        else:
            stats = updater.update_all_artists(batch_size=batch_size)
        
        # Print results
        self.stdout.write(self.style.SUCCESS(
            f"Update completed: {stats['updated']} updated, {stats['failed']} failed, {stats['skipped']} skipped"
        ))