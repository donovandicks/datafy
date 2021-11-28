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
