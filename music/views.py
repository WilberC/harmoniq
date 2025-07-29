"""
Views for the music app.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, models
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json

from .models import Playlist, Track, MusicService
from .serializers import PlaylistSerializer, TrackSerializer


@login_required
def dashboard(request):
    """Main dashboard view with Finder-like interface"""
    playlists = Playlist.objects.filter(user=request.user)
    
    # Get the selected playlist
    selected_playlist_id = request.GET.get('playlist')
    selected_playlist = None
    tracks = []
    
    if selected_playlist_id:
        selected_playlist = get_object_or_404(Playlist, id=selected_playlist_id, user=request.user)
        tracks = selected_playlist.tracks.all()
    
    context = {
        'playlists': playlists,
        'selected_playlist': selected_playlist,
        'tracks': tracks,
    }
    
    return render(request, 'music/dashboard.html', context)


@login_required
def playlist_detail(request, playlist_id):
    """Detail view for a specific playlist"""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    tracks = playlist.tracks.all()
    
    context = {
        'playlist': playlist,
        'tracks': tracks,
    }
    
    return render(request, 'music/playlist_detail.html', context)


@login_required
@require_http_methods(["POST"])
def create_playlist(request):
    """Create a new playlist"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        color = request.POST.get('color', '#3B82F6')
        
        if name:
            playlist = Playlist.objects.create(
                user=request.user,
                name=name,
                description=description,
                color=color
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'playlist': {
                        'id': playlist.id,
                        'name': playlist.name,
                        'color': playlist.color,
                        'track_count': 0
                    }
                })
            else:
                messages.success(request, f'Playlist "{name}" created successfully!')
                return redirect('dashboard')
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
@require_http_methods(["POST"])
def delete_playlist(request, playlist_id):
    """Delete a playlist"""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    playlist_name = playlist.name
    playlist.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    else:
        messages.success(request, f'Playlist "{playlist_name}" deleted successfully!')
        return redirect('dashboard')


@login_required
@require_http_methods(["POST"])
def add_track(request, playlist_id):
    """Add a track to a playlist"""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        album = request.POST.get('album', '')
        duration = request.POST.get('duration', 0)
        
        if title and artist:
            # Get the next position
            max_position = playlist.tracks.aggregate(models.Max('position'))['position__max'] or 0
            position = max_position + 1
            
            track = Track.objects.create(
                user=request.user,
                playlist=playlist,
                title=title,
                artist=artist,
                album=album,
                duration=int(duration) if duration else 0,
                position=position
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'track': {
                        'id': track.id,
                        'title': track.title,
                        'artist': track.artist,
                        'album': track.album,
                        'duration': track.duration_formatted,
                        'position': track.position
                    }
                })
            else:
                messages.success(request, f'Track "{title}" added to playlist!')
                return redirect('playlist_detail', playlist_id=playlist.id)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
@require_http_methods(["POST"])
def delete_track(request, track_id):
    """Delete a track"""
    track = get_object_or_404(Track, id=track_id, user=request.user)
    track_title = track.title
    playlist_id = track.playlist.id
    track.delete()
    
    # Reorder remaining tracks
    playlist = track.playlist
    for i, remaining_track in enumerate(playlist.tracks.order_by('position')):
        remaining_track.position = i + 1
        remaining_track.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    else:
        messages.success(request, f'Track "{track_title}" deleted successfully!')
        return redirect('playlist_detail', playlist_id=playlist_id)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def move_track(request):
    """Move a track to a different position or playlist"""
    try:
        data = json.loads(request.body)
        track_id = data.get('track_id')
        new_playlist_id = data.get('new_playlist_id')
        new_position = data.get('new_position')
        
        track = get_object_or_404(Track, id=track_id, user=request.user)
        new_playlist = get_object_or_404(Playlist, id=new_playlist_id, user=request.user)
        
        with transaction.atomic():
            # Remove track from old position
            old_playlist = track.playlist
            old_position = track.position
            
            # Update positions in old playlist
            old_playlist.tracks.filter(position__gt=old_position).update(
                position=models.F('position') - 1
            )
            
            # Update positions in new playlist
            new_playlist.tracks.filter(position__gte=new_position).update(
                position=models.F('position') + 1
            )
            
            # Move track to new position
            track.playlist = new_playlist
            track.position = new_position
            track.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Track moved to {new_playlist.name}'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def reorder_tracks(request, playlist_id):
    """Reorder tracks within a playlist"""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        track_order = data.get('track_order', [])
        
        with transaction.atomic():
            for position, track_id in enumerate(track_order, 1):
                track = get_object_or_404(Track, id=track_id, playlist=playlist, user=request.user)
                track.position = position
                track.save()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
def music_services(request):
    """View for managing music service connections"""
    services = MusicService.objects.filter(user=request.user)
    
    context = {
        'services': services,
        'available_services': MusicService.SERVICE_CHOICES,
    }
    
    return render(request, 'music/music_services.html', context)


# API Views for AJAX functionality
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_playlists(request):
    """API endpoint to get all playlists for the user"""
    playlists = Playlist.objects.filter(user=request.user)
    serializer = PlaylistSerializer(playlists, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_playlist_tracks(request, playlist_id):
    """API endpoint to get tracks for a specific playlist"""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    tracks = playlist.tracks.all()
    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_move_track(request):
    """API endpoint to move a track"""
    return move_track(request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_reorder_tracks(request, playlist_id):
    """API endpoint to reorder tracks in a playlist"""
    return reorder_tracks(request, playlist_id)