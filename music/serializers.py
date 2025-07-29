"""
Serializers for the music app.
"""
from rest_framework import serializers
from .models import Playlist, Track, MusicService


class TrackSerializer(serializers.ModelSerializer):
    """Serializer for Track model"""
    duration_formatted = serializers.ReadOnlyField()
    
    class Meta:
        model = Track
        fields = [
            'id', 'title', 'artist', 'album', 'duration', 
            'duration_formatted', 'external_id', 'external_url', 
            'album_art_url', 'position', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']


class PlaylistSerializer(serializers.ModelSerializer):
    """Serializer for Playlist model"""
    track_count = serializers.ReadOnlyField()
    tracks = TrackSerializer(many=True, read_only=True)
    
    class Meta:
        model = Playlist
        fields = [
            'id', 'name', 'description', 'color', 'icon', 
            'position', 'is_favorite', 'created_at', 'updated_at',
            'track_count', 'tracks'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MusicServiceSerializer(serializers.ModelSerializer):
    """Serializer for MusicService model"""
    service_display = serializers.CharField(source='get_service_display', read_only=True)
    
    class Meta:
        model = MusicService
        fields = [
            'id', 'service', 'service_display', 'external_user_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlaylistCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating playlists"""
    
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'color', 'icon']


class TrackCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tracks"""
    
    class Meta:
        model = Track
        fields = ['title', 'artist', 'album', 'duration', 'external_id', 'external_url', 'album_art_url']


class TrackMoveSerializer(serializers.Serializer):
    """Serializer for moving tracks"""
    track_id = serializers.IntegerField()
    new_playlist_id = serializers.IntegerField()
    new_position = serializers.IntegerField(min_value=1)


class TrackReorderSerializer(serializers.Serializer):
    """Serializer for reordering tracks"""
    track_order = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )