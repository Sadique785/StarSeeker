from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=255)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=255)
    popularity = models.IntegerField(default=0) 


    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['genre']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.name
    
    def get_popularity(self):

        return self.popularity

class NewArtist(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=255)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['genre']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.name