# serializers.py
from rest_framework import serializers
from ..models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'genre', 'profile_picture', 'location', 'get_popularity']