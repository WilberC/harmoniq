"""
Models for the music app.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class MusicService(models.Model):
    """Model for music service connections (Spotify, Tidal, etc.)"""
    SERVICE_CHOICES = [
        ('spotify', 'Spotify'),
        ('tidal', 'Tidal'),
        ('apple_music', 'Apple Music'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    token_expires_at = models.DateTimeField()
    external_user_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'service']
    
    def __str__(self):
        return f"{self.user.username} - {self.service}"


class Playlist(models.Model):
    """Model for playlists (folders in Finder-like interface)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    icon = models.CharField(max_length=50, default='folder')  # Icon name
    position = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['position', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def track_count(self):
        return self.tracks.count()


class Track(models.Model):
    """Model for music tracks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    duration = models.IntegerField(default=0)  # Duration in seconds
    external_id = models.CharField(max_length=255, blank=True)  # ID from music service
    external_url = models.URLField(blank=True)  # URL to track on music service
    album_art_url = models.URLField(blank=True)
    position = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['playlist', 'position']
        unique_together = ['playlist', 'position']
    
    def __str__(self):
        return f"{self.title} - {self.artist}"
    
    @property
    def duration_formatted(self):
        """Return duration in MM:SS format"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"


class PlaylistShare(models.Model):
    """Model for sharing playlists between users"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_playlists')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_playlists')
    can_edit = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['playlist', 'shared_with']
    
    def __str__(self):
        return f"{self.playlist.name} shared by {self.shared_by.username}"