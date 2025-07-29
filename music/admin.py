"""
Admin configuration for the music app.
"""
from django.contrib import admin
from .models import Playlist, Track, MusicService, PlaylistShare


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'track_count', 'is_favorite', 'created_at']
    list_filter = ['is_favorite', 'created_at', 'user']
    search_fields = ['name', 'description', 'user__username']
    ordering = ['-created_at']
    
    def track_count(self, obj):
        return obj.track_count
    track_count.short_description = 'Tracks'


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'album', 'playlist', 'user', 'position', 'duration_formatted']
    list_filter = ['playlist', 'added_at', 'user']
    search_fields = ['title', 'artist', 'album', 'playlist__name']
    ordering = ['playlist', 'position']
    
    def duration_formatted(self, obj):
        return obj.duration_formatted
    duration_formatted.short_description = 'Duration'


@admin.register(MusicService)
class MusicServiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'external_user_id', 'created_at']
    list_filter = ['service', 'created_at']
    search_fields = ['user__username', 'external_user_id']
    ordering = ['-created_at']
    
    def get_readonly_fields(self, request, obj=None):
        return ['access_token', 'refresh_token', 'token_expires_at']


@admin.register(PlaylistShare)
class PlaylistShareAdmin(admin.ModelAdmin):
    list_display = ['playlist', 'shared_by', 'shared_with', 'can_edit', 'shared_at']
    list_filter = ['can_edit', 'shared_at']
    search_fields = ['playlist__name', 'shared_by__username', 'shared_with__username']
    ordering = ['-shared_at']