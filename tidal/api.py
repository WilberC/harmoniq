import base64
import hashlib
import logging
import os
import secrets
import time
import urllib.parse
from datetime import timedelta

import requests
from django.utils import timezone

from .models import TidalToken

logger = logging.getLogger(__name__)


class TidalTokenManager:
    """
    Manages Tidal API access tokens with automatic caching and renewal.
    """

    def __init__(self):
        self.client_id = os.getenv("TIDAL_CLIENT_ID")
        self.client_secret = os.getenv("TIDAL_CLIENT_SECRET")
        self.token_url = os.getenv("TIDAL_AUTH")
        self._access_token = None
        self._token_type = None
        self._expiry_time = None

    def _fetch_token(self):
        """
        Fetches a new access token from Tidal API.
        """
        if not self.client_id or not self.client_secret:
            raise ValueError("TIDAL_CLIENT_ID and TIDAL_CLIENT_SECRET must be set in settings")

        # Encode credentials
        credentials = f"{self.client_id}:{self.client_secret}"
        b64_creds = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_creds}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {"grant_type": "client_credentials"}

        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()

        self._access_token = token_data.get("access_token")
        self._token_type = token_data.get("token_type")
        expires_in = token_data.get("expires_in", 0)
        self._expiry_time = time.time() + expires_in

        if not self._access_token or not self._token_type:
            raise ValueError("Invalid token response from Tidal API")

    def get_token(self):
        """
        Returns the current valid access token, fetching a new one if necessary.
        Renews if the token expires in less than 60 seconds.
        """
        current_time = time.time()

        if (
            self._access_token is None
            or self._expiry_time is None
            or current_time >= self._expiry_time - 60
        ):
            self._fetch_token()

        return f"{self._token_type} {self._access_token}"

    def get_user_token(self, user):
        """
        Returns the current valid access token for a user, refreshing if necessary.
        """
        try:
            tidal_token = TidalToken.objects.get(user=user)

            # Check if token is expired or will expire in the next 5 minutes
            current_time = timezone.now()
            buffer_time = timedelta(minutes=5)

            if tidal_token.is_expired() or tidal_token.expires_at <= current_time + buffer_time:
                # Token is expired or will expire soon, try to refresh
                if tidal_token.refresh_token:
                    try:
                        logger.info(f"Refreshing expired token for user: {user.username}")
                        oauth_manager = TidalOAuthManager()
                        new_token_data = oauth_manager.refresh_access_token(
                            tidal_token.refresh_token
                        )

                        # Update the token in database
                        tidal_token.access_token = new_token_data["access_token"]
                        if new_token_data.get("refresh_token"):
                            tidal_token.refresh_token = new_token_data["refresh_token"]
                        tidal_token.expires_at = timezone.now() + timedelta(
                            seconds=new_token_data["expires_in"]
                        )
                        tidal_token.save()

                        logger.info(f"Token refreshed successfully for user: {user.username}")
                        return f"Bearer {tidal_token.access_token}"

                    except Exception as e:
                        logger.error(f"Failed to refresh token for user {user.username}: {e}")
                        # If refresh fails, return None to indicate token is invalid
                        return None
                else:
                    # No refresh token available
                    logger.warning(f"No refresh token available for user: {user.username}")
                    return None

            return f"Bearer {tidal_token.access_token}"

        except TidalToken.DoesNotExist:
            logger.info(f"No Tidal token found for user: {user.username}")
            return None

    def save_user_token(self, user, token_data):
        """
        Saves or updates the user's Tidal token in the database.
        """
        expires_at = timezone.now() + timedelta(seconds=token_data["expires_in"])

        tidal_token, created = TidalToken.objects.get_or_create(
            user=user,
            defaults={
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token"),
                "expires_at": expires_at,
            },
        )

        if not created:
            # Update existing token
            tidal_token.access_token = token_data["access_token"]
            tidal_token.refresh_token = token_data.get("refresh_token")
            tidal_token.expires_at = expires_at
            tidal_token.save()

        return tidal_token

    def refresh_user_token(self, user):
        """
        Manually refresh a user's access token.
        Returns True if successful, False if refresh token is invalid/expired.
        """
        try:
            tidal_token = TidalToken.objects.get(user=user)

            if not tidal_token.refresh_token:
                logger.warning(f"No refresh token available for user: {user.username}")
                return False

            try:
                logger.info(f"Manually refreshing token for user: {user.username}")
                oauth_manager = TidalOAuthManager()
                new_token_data = oauth_manager.refresh_access_token(tidal_token.refresh_token)

                # Update the token in database
                tidal_token.access_token = new_token_data["access_token"]
                if new_token_data.get("refresh_token"):
                    tidal_token.refresh_token = new_token_data["refresh_token"]
                tidal_token.expires_at = timezone.now() + timedelta(
                    seconds=new_token_data["expires_in"]
                )
                tidal_token.save()

                logger.info(f"Token refreshed successfully for user: {user.username}")
                return True

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 400:
                    # Refresh token is likely expired or invalid
                    logger.warning(f"Refresh token expired for user: {user.username}")
                    # Optionally delete the invalid token
                    tidal_token.delete()
                else:
                    logger.error(f"HTTP error during token refresh for user {user.username}: {e}")
                return False

            except Exception as e:
                logger.error(f"Failed to refresh token for user {user.username}: {e}")
                return False

        except TidalToken.DoesNotExist:
            logger.info(f"No Tidal token found for user: {user.username}")
            return False

    def get_valid_user_token(self, user):
        """
        Gets a valid access token for a user, handling refresh automatically.
        This is the main method API consumers should use.
        Returns the token string or None if no valid token available.
        """
        token = self.get_user_token(user)
        if token:
            return token

        # If get_user_token returned None, try manual refresh
        if self.refresh_user_token(user):
            return self.get_user_token(user)

        return None


class PKCE:
    """
    Handles PKCE (Proof Key for Code Exchange) code verifier and challenge generation.
    """

    @staticmethod
    def generate_code_verifier():
        """
        Generates a cryptographically random code verifier.
        Returns a URL-safe string of 43-128 characters.
        """
        # Generate 32 bytes (256 bits) of random data
        verifier_bytes = secrets.token_bytes(32)
        # Base64url encode (RFC 4648)
        verifier = base64.urlsafe_b64encode(verifier_bytes).decode("ascii").rstrip("=")
        return verifier

    @staticmethod
    def generate_code_challenge(verifier):
        """
        Generates the code challenge from the code verifier using S256 method.
        """
        # SHA256 hash of the verifier
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        # Base64url encode the hash
        challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
        return challenge


class TidalOAuthManager:
    """
    Manages Tidal OAuth 2.1 authorization code flow with PKCE.
    """

    def __init__(self):
        self.client_id = os.getenv("TIDAL_CLIENT_ID")
        self.client_secret = os.getenv("TIDAL_CLIENT_SECRET")
        self.redirect_uri = os.getenv("TIDAL_REDIRECT_URI")
        self.authorize_url = os.getenv("TIDAL_AUTHORIZE_URL")
        self.token_url = os.getenv("TIDAL_AUTH")
        self.scopes = os.getenv("TIDAL_SCOPES", "r_usr w_usr")

    def get_authorization_url(self, state=None):
        """
        Generates the authorization URL for Tidal login.
        Returns the URL and the code verifier (store this for later token exchange).
        """
        if not all([self.client_id, self.redirect_uri, self.authorize_url]):
            raise ValueError(
                "TIDAL_CLIENT_ID, TIDAL_REDIRECT_URI, and TIDAL_AUTHORIZE_URL must be set"
            )

        # Generate PKCE values
        code_verifier = PKCE.generate_code_verifier()
        code_challenge = PKCE.generate_code_challenge(code_verifier)

        # Generate state if not provided
        if state is None:
            state = secrets.token_urlsafe(32)

        # Build authorization URL
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
            "state": state,
        }

        query_string = urllib.parse.urlencode(params)
        authorization_url = f"{self.authorize_url}?{query_string}"

        return authorization_url, code_verifier, state

    def exchange_code_for_token(self, authorization_code, code_verifier):
        """
        Exchanges the authorization code for access and refresh tokens.
        """
        if not all([self.client_id, self.client_secret, self.token_url]):
            raise ValueError("TIDAL_CLIENT_ID, TIDAL_CLIENT_SECRET, and TIDAL_AUTH must be set")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier,
        }

        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()

        # Validate required fields
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in", 86400)  # Default 24 hours

        if not access_token:
            raise ValueError("No access_token in response")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
            "token_type": token_data.get("token_type", "Bearer"),
            "scope": token_data.get("scope"),
        }

    def refresh_access_token(self, refresh_token):
        """
        Refreshes an access token using a refresh token.
        """
        if not all([self.client_id, self.client_secret, self.token_url]):
            raise ValueError("TIDAL_CLIENT_ID, TIDAL_CLIENT_SECRET, and TIDAL_AUTH must be set")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
        }

        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()

        # Validate required fields
        access_token = token_data.get("access_token")
        new_refresh_token = token_data.get("refresh_token")  # May be None if not provided
        expires_in = token_data.get("expires_in", 86400)  # Default 24 hours

        if not access_token:
            raise ValueError("No access_token in refresh response")

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token
            or refresh_token,  # Use new one if provided, otherwise keep old
            "expires_in": expires_in,
            "token_type": token_data.get("token_type", "Bearer"),
            "scope": token_data.get("scope"),
        }


def get_tidal_token_for_user(user):
    """
    Helper function to get a valid Tidal access token for a user.
    Automatically handles token refresh if needed.
    """
    token_manager = TidalTokenManager()
    return token_manager.get_valid_user_token(user)
