"""Defines the base Spotify service with configurations"""

from abc import abstractmethod
from os import getenv
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import HTTPException
from models.common import Query
from models.rec import RecQuery
from pymongo import MongoClient
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

    @property
    def query(self) -> Query:
        """The query attr"""
        return self._query

    @query.setter
    def query(self, item_query):
        """"""
        self._query = item_query

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

    @abstractmethod
    def get_genres_from_spotify(self) -> List[str]:
        """Should retrieve a list of genres"""

    @abstractmethod
    def get_recommendations_from_spotify(self) -> List[Dict]:
        """Should retrieve a list of recommendations"""


class Client(SpotifyClient):
    """Concrete implementation of a Spotify client"""

    def __init__(self, item_query: Query) -> None:
        self.client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=settings["client_id"],
                client_secret=settings["client_secret"],
                redirect_uri="http://localhost:8080",
                scope=settings["scopes"],
            )
        )
        self.db_client = MongoClient(getenv("CONNECTIONSTRING"))
        self.__database = self.db_client.get_database("datafy")
        self.artists_collection = self.__database.get_collection("artists")
        self.songs_collection = self.__database.get_collection("songs")
        self.query = item_query

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
        found = self.artists_collection.find_one({"id": artist_id})
        if found:
            return found

        artist = self.client.artist(artist_id)
        if not artist:
            raise HTTPException(404, f"Artist {artist_id} not found")

        self.artists_collection.insert_one(artist)
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
        found = self.songs_collection.find_one({"id": song_id})
        if found:
            return found

        song = self.client.track(song_id)
        if not song:
            raise HTTPException(404, "Song not found")

        self.songs_collection.insert_one(song)
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

    def get_genres_from_spotify(self) -> List[str]:
        """
        Retrieves a count of the occurrences of genres for the current users top artists

        Params
        ------
        time_range: Optional[TimeRange]
            the time_range parameter from which to retrieve results
        client: Spotify
            the api client used to connect to spotify

        Returns
        -------
        genre_detail: Dict[str, int]
            an object mapping a genre name to a count of its appearance

        Raises
        ------
        HTTPException(404)
            if the client is unable to retrieve any results
        """
        top_artists = self.client.current_user_top_artists(
            limit=50,
            time_range=self.query.time_range,
        )

        if not top_artists:
            raise HTTPException(404, "Top genres not found")

        genre_detail = []
        for item in top_artists["items"]:
            genre_detail.extend(item["genres"])

        return genre_detail

    def get_recommendations_from_spotify(self) -> List[Dict]:
        """
        Retrieves recommendations from spotify

        Params
        ------
        query: RecQuery
            the query object containing seed data for the recommendation api
        client: [Spotify]
            the api client object used to interact with Spotify

        Returns
        -------
        tracks: List[Dict]
            a list of tracks returned from the API
        """
        if not isinstance(self.query, RecQuery):
            raise TypeError("Invalid query type for recommendations")

        recommendations = self.client.recommendations(
            seed_artists=self.query.seed_artists_list,
            seed_genres=self.query.seed_genres_list,
            seed_tracks=self.query.seed_tracks_list,
            limit=self.query.limit,
        )

        if not recommendations:
            raise HTTPException(404, "Recommendations not found")

        return recommendations["tracks"]
