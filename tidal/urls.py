from django.urls import path

from . import views

app_name = "tidal"

urlpatterns = [
    path("login/", views.tidal_login, name="tidal_login"),
    path("auth/callback/", views.tidal_callback, name="tidal_callback"),
    path("playlists/", views.user_playlists, name="tidal_playlists"),
    path("playlists/<str:playlist_id>/", views.playlist_tracks, name="playlist_tracks"),
]
