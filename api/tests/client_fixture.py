"""Defines the test client"""

from typing import Any, Dict, List, Optional

from dependencies.spotify import SpotifyClient
from models.common import Query


class FakeClient(SpotifyClient):
    """Test implementation of the SpotifyClient Interface"""

    def __init__(self, query: Optional[Query]) -> None:
        self.query = query

    def get_artists_from_spotify(self) -> List[Dict]:
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
        return [
            {
                "id": "ABC123",
                "name": "Jimbo",
                "popularity": 99,
                "followers": {"total": 1234567},
                "genres": ["folk"],
                "other_field": "not_parsed",
            },
            {
                "id": "DEF456",
                "name": "Jimothy",
                "popularity": 97,
                "followers": {"total": 1234234},
                "genres": ["pop"],
                "other_field": "not_parsed",
            },
        ]

    def get_artist_from_spotify(self, artist_id: str) -> Dict[str, Any]:
        return {
            "id": "ABC123",
            "name": "Jimbo",
            "popularity": 99,
            "followers": {"total": 1234567},
            "genres": ["folk"],
            "other_field": "not_parsed",
        }

    def get_songs_from_spotify(self) -> List[Dict]:
        return [
            {
                "id": "ABC123",
                "name": "Love Song",
                "artists": [{"name": "Wesley"}],
                "popularity": 99,
                "album": {
                    "name": "The Princess Bride",
                    "release_date": "1987-09-07",
                },
                "other_field": "not_parsed",
            },
            {
                "id": "DEF456",
                "name": "Pirate Song",
                "artists": [{"name": "Jack Sparrow"}],
                "popularity": 95,
                "album": {
                    "name": "Pirates of the Carribean",
                    "release_date": "2001-05-15",
                },
                "other_field": "not_parsed",
            },
        ]

    def get_song_from_spotify(self, song_id: str) -> Dict:
        return {
            "id": song_id,
            "name": "Love Song",
            "artists": [{"name": "Wesley"}],
            "popularity": 99,
            "album": {"name": "The Princess Bride", "release_date": "1987-09-07"},
            "other_field": "not_parsed",
        }

    def get_genres_from_spotify(self) -> List[str]:
        return [
            "rap",
            "hip hop",
            "underground hip hop",
            "hip hop",
            "alternative hip hop",
            "rap",
            "hip hop",
            "underground hip hop",
            "rap",
            "hip hop",
            "underground hip hop",
            "hip hop",
            "alternative hip hop",
            "rap",
            "pop rap",
            "rap",
            "pop rap",
            "pop",
            "pop",
            "pop",
        ]

    def get_recommendations_from_spotify(self) -> List[Dict]:
        return [
            {"name": "Erase Your Social", "artists": [{"name": "Lil Uzi Vert"}]},
            {
                "name": "Flex",
                "artists": [{"name": "Playboi Carti"}, {"name": "Leven Kali"}],
            },
            {"name": "Self Care", "artists": [{"name": "Mac Miller"}]},
        ]
