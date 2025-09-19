import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .api import TidalAPIClient, TidalOAuthManager, TidalTokenManager

logger = logging.getLogger(__name__)


def auto_login_test_user(request):
    from django.contrib.auth import login
    from django.contrib.auth.models import User

    user, created = User.objects.get_or_create(username="testuser")
    if created:
        user.set_password("testpassword")
        user.save()
    login(request, user)
    return redirect(reverse("index"))


@require_GET
def tidal_login(request):
    """
    Initiates the Tidal OAuth authorization flow.
    Generates PKCE values and redirects to Tidal login.
    """
    auto_login_test_user(request)  # Auto-login for testing purposes
    oauth_manager = TidalOAuthManager()

    try:
        authorization_url, code_verifier, state = oauth_manager.get_authorization_url()

        # Store values in session for later use in callback
        request.session["tidal_code_verifier"] = code_verifier
        request.session["tidal_state"] = state

        logger.info(f"Tidal login initiated. URL: {authorization_url}")
        logger.info(f"Code verifier stored in session: {code_verifier[:10]}...")
        logger.info(f"State stored in session: {state[:10]}...")

        return redirect(authorization_url)

    except ValueError as e:
        return HttpResponseBadRequest(f"OAuth configuration error: {e}")


@require_GET
@login_required
def tidal_callback(request):
    """
    Handles the OAuth callback from Tidal.
    Exchanges authorization code for tokens and saves them.
    """
    # Get parameters from the callback
    authorization_code = request.GET.get("code")
    state = request.GET.get("state")
    error = request.GET.get("error")
    error_description = request.GET.get("error_description")

    # Check for errors
    if error:
        logger.error(f"Tidal OAuth error: {error} - {error_description}")
        return HttpResponseBadRequest(f"Tidal OAuth error: {error} - {error_description}")

    if not authorization_code:
        logger.error("No authorization code received in callback")
        return HttpResponseBadRequest("No authorization code received")

    # Validate state parameter
    session_state = request.session.get("tidal_state")
    if not session_state or state != session_state:
        logger.error(f"State mismatch. Received: {state}, Expected: {session_state}")
        return HttpResponseBadRequest("Invalid state parameter")

    logger.info(f"Authorization code received: {authorization_code[:10]}...")
    logger.info("State validation successful")

    # Get code verifier from session
    code_verifier = request.session.get("tidal_code_verifier")
    if not code_verifier:
        return HttpResponseBadRequest("Code verifier not found in session")

    # Clear session values
    del request.session["tidal_state"]
    del request.session["tidal_code_verifier"]

    # Exchange code for tokens
    oauth_manager = TidalOAuthManager()
    token_manager = TidalTokenManager()

    try:
        logger.info(f"Exchanging code for tokens with verifier: {code_verifier[:10]}...")
        token_data = oauth_manager.exchange_code_for_token(authorization_code, code_verifier)

        logger.info(
            f"Token exchange successful. Access token: {token_data.get('access_token', '')[:10]}..."
        )

        # Save tokens to database
        token_manager.save_user_token(request.user, token_data)
        token_manager.save_tidal_user_id(request.user)

        logger.info(f"Tokens saved for user: {request.user.username}")

        # Redirect to success page (you can customize this)
        return redirect(reverse("index"))  # or wherever you want to redirect after successful auth

    except Exception as e:
        logger.error(f"Token exchange failed: {e}")
        return HttpResponseBadRequest(f"Token exchange failed: {e}")


def user_playlists(request):
    """
    Display user's Tidal playlists in a folder-like interface.
    """
    try:
        api_client = TidalAPIClient()
        playlists = api_client.get_user_playlists(request.user)

        context = {"playlists": playlists, "current_path": "My Playlists"}
        return render(request, "tidal/playlists.html", context)

    except Exception as e:
        logger.error(f"Failed to fetch playlists for user {request.user.username}: {e}")
        messages.error(request, f"Failed to load playlists: {e}")
        return redirect("index")


def playlist_tracks(request, playlist_id):
    """
    Display tracks from a specific playlist.
    """
    try:
        api_client = TidalAPIClient()

        # Get playlist details and tracks
        playlist_details = api_client.get_playlist_details(request.user, playlist_id)
        tracks = api_client.get_playlist_tracks(request.user, playlist_id)

        context = {
            "playlist": playlist_details,
            "tracks": tracks,
            "current_path": f"My Playlists / {playlist_details.get('title', 'Unknown Playlist')}",
            "playlist_id": playlist_id,
        }

        return render(request, "tidal/playlist_tracks.html", context)

    except Exception as e:
        logger.error(f"Failed to fetch playlist tracks for playlist {playlist_id}: {e}")
        messages.error(request, f"Failed to load playlist: {e}")
        return redirect("tidal_playlists")
