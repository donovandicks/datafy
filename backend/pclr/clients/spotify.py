"""Code for interacting with Spotify"""

import os


from dotenv import load_dotenv
from spotipy import Spotify, SpotifyOAuth

load_dotenv()


def init_spotify_client() -> Spotify:
    """Initializes a Spotipy instance with local credentials"""
    return Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID", ""),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET", ""),
            redirect_uri="http://localhost:8080",
            scope="user-read-currently-playing",
        )
    )
