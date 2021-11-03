"""Defines the base Spotify service with configurations"""

from os import getenv

from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()


settings = {
    "scopes": "  ".join(
        [
            "ugc-image-upload",
            "playlist-modify-private",
            "playlist-read-private",
            "playlist-modify-public",
            "playlist-read-collaborative",
            "user-read-private",
            "user-read-playback-state",
            "user-modify-playback-state",
            "user-read-currently-playing",
            "user-library-modify",
            "user-library-read",
            "user-read-playback-position",
            "user-read-recently-played",
            "user-top-read",
            "app-remote-control",
            "streaming",
            "user-follow-modify",
            "user-follow-read",
        ]
    ),
    "client_id": getenv("CLIENT_ID"),
    "client_secret": getenv("CLIENT_SECRET"),
    "redirect_uri": getenv("REDIRECT_URI"),
}


class BaseService:
    """Defines a service that initializes the Spotify client"""

    def __init__(self) -> None:
        self.client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=settings["client_id"],
                client_secret=settings["client_secret"],
                redirect_uri=settings["redirect_uri"],
                scope=settings["scopes"],
            )
        )
