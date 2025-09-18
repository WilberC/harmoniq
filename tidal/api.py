import base64
import os
import time

import requests


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
