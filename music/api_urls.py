"""
API URL configuration for the music app.
"""
from django.urls import path
from . import views

app_name = 'music_api'

urlpatterns = [
    # API endpoints
    path('playlists/', views.api_playlists, name='api_playlists'),
    path('playlists/<int:playlist_id>/tracks/', views.api_playlist_tracks, name='api_playlist_tracks'),
    path('tracks/move/', views.api_move_track, name='api_move_track'),
    path('playlists/<int:playlist_id>/reorder/', views.api_reorder_tracks, name='api_reorder_tracks'),
]