"""
URL configuration for the music app.
"""
from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    # Main views
    path('', views.dashboard, name='dashboard'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('services/', views.music_services, name='music_services'),
    
    # Playlist actions
    path('playlist/create/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    
    # Track actions
    path('playlist/<int:playlist_id>/add-track/', views.add_track, name='add_track'),
    path('track/<int:track_id>/delete/', views.delete_track, name='delete_track'),
    path('track/move/', views.move_track, name='move_track'),
    path('playlist/<int:playlist_id>/reorder/', views.reorder_tracks, name='reorder_tracks'),
]