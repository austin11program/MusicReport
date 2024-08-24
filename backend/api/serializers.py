from rest_framework import serializers
from .models import TrackInfo



class TrackInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackInfo
        fields = ["id", "songName", "artistName", "albumName","coverUrls","previewUrl"] 
        
     