"""Defines the base Spotify service with configurations"""

from abc import abstractmethod
from os import getenv
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import HTTPException
from models.common import Query
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
}

CLIENT = Spotify(
    auth_manager=SpotifyOAuth(
        client_id=settings["client_id"],
        client_secret=settings["client_secret"],
        redirect_uri="http://localhost:8080",
        scope=settings["scopes"],
    )
)


class SpotifyClient:
    """Interface describing methods to interact with Spotify"""

    @abstractmethod
    def get_artists_from_spotify(self) -> List[Dict]:
        """Should retrieve a list of artists"""

    @abstractmethod
    def get_artist_from_spotify(self, artist_id: str) -> Dict[str, Any]:
        """Should retrieve a single artist"""

    @abstractmethod
    def get_song_from_spotify(self, song_id: str) -> Dict:
        """Should retrieve a single song"""

    @abstractmethod
    def get_songs_from_spotify(self) -> List[Dict]:
        """Should retrieve a list of songs"""


class Client(SpotifyClient):
    """Concrete implementation of a Spotify client"""

    def __init__(self, query: Query) -> None:
        self.client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=settings["client_id"],
                client_secret=settings["client_secret"],
                redirect_uri="http://localhost:8080",
                scope=settings["scopes"],
            )
        )
        self.query = query

    def get_artists_from_spotify(self) -> List:
        """
        Retrieves the current users top artists from spotify

        Returns
        -------
        top_artists: List
            a list of spotify artist objects retrieved from the api

        Raises
        ------
        HTTPException(404)
            if no top artists are found for the current user
        """
        top_artists = self.client.current_user_top_artists(
            limit=self.query.limit,
            time_range=self.query.time_range,
        )

        if not top_artists:
            raise HTTPException(404, "Top artists not found")

        return top_artists["items"]

    def get_artist_from_spotify(self, artist_id: str) -> Dict[str, Any]:
        """
        Retrieves a single artist from spotify

        Params
        ------
        artist_id: str
            the spotify ID, URI, or URL of the artist

        Returns
        -------
        artist: Dict
            the artist object
        client: [Spotify]
            the api client used to connect to spotify

        Raises
        ------
        HTTPException(404)
            if no artist is found for the ID
        """

        artist = self.client.artist(artist_id)

        if not artist:
            raise HTTPException(404, f"Artist {artist_id} not found")

        return artist

    def get_song_from_spotify(self, song_id: str) -> Dict:
        """
        Retrieves a single song from spotify

        Params
        ------
        song_id: str
            the spotify ID, URI, or URL for the song
        client: [Spotify]
            the api client used to connect to spotify

        Raises
        ------
        HTTPException(404)
            if the song is not found
        """
        song = self.client.track(song_id)

        if not song:
            raise HTTPException(404, "Song not found")

        return song

    def get_songs_from_spotify(self) -> List[Dict]:
        """
        Retrieves the current users top songs from spotify

        Returns
        -------
        top_songs: List[Dict]
            a  list of spotify song objects from the api

        Raises
        ------
        HTTPException(404)
            if no top songs are found
        """
        top_songs = self.client.current_user_top_tracks(
            limit=self.query.limit, time_range=self.query.time_range
        )

        if not top_songs:
            raise HTTPException(404, "Top songs not found")

        return top_songs["items"]
