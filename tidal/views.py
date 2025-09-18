from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from .api import TidalOAuthManager, TidalTokenManager


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

        print(f"Redirecting to Tidal authorization URL: {authorization_url}")
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
        return HttpResponseBadRequest(f"Tidal OAuth error: {error} - {error_description}")

    if not authorization_code:
        return HttpResponseBadRequest("No authorization code received")

    # Validate state parameter
    session_state = request.session.get("tidal_state")
    if not session_state or state != session_state:
        return HttpResponseBadRequest("Invalid state parameter")

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
        token_data = oauth_manager.exchange_code_for_token(authorization_code, code_verifier)

        # Save tokens to database
        token_manager.save_user_token(request.user, token_data)

        # Redirect to success page (you can customize this)
        return redirect(reverse("index"))  # or wherever you want to redirect after successful auth

    except Exception as e:
        return HttpResponseBadRequest(f"Token exchange failed: {e}")
