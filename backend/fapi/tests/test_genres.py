"""Test Suite for the `/genres` route"""
from typing import Dict, List, Optional
from unittest import TestCase

from models.common import TimeRange
from models.genre import Genre, GenreQuery
from routers import genres


def retriever(_: Optional[TimeRange]) -> Dict[str, int]:
    """
    Test impl of a retriever
    """
    return {
        "rap": 5,
        "hip hop": 5,
        "underground hip hop": 3,
        "alternative hip hop": 2,
        "pop": 3,
        "pop rap": 2,
    }


class Client:
    """Test impl of the Spotipy client"""

    def current_user_top_artists(self, limit, time_range) -> Dict[str, List]:
        """Test impl of Spotipy.current_user_top_artists"""
        return {
            "items": [
                {"genres": ["rap", "hip hop", "underground hip hop"]},
                {"genres": ["hip hop", "alternative hip hop"]},
                {"genres": ["rap", "hip hop", "underground hip hop"]},
                {"genres": ["rap", "hip hop", "underground hip hop"]},
                {"genres": ["hip hop", "alternative hip hop"]},
                {"genres": ["rap", "pop rap"]},
                {"genres": ["rap", "pop rap"]},
                {"genres": ["pop"]},
                {"genres": ["pop"]},
                {"genres": ["pop"]},
            ]
        }


class GenresTest(TestCase):
    """Unit tests for the genres logic"""

    def test_get_genre_aggregate(self):
        """Tests both get_genre_aggregate and get_genres_from_spotify"""
        self.assertEqual(
            {
                "hip hop": 10,
                "rap": 7,
                "pop": 5,
                "electronic": 0,
                "country": 0,
                "folk": 0,
                "indie": 0,
                "metal": 0,
                "r&b": 0,
                "rock": 0,
                "soul": 0,
                "jazz": 0,
                "classical": 0,
            },
            genres.get_genre_aggregate(
                genres.get_genres_from_spotify(TimeRange.MEDIUM_TERM, Client())
            ),
        )

    def test_get_genre_detail(self):
        """Tests get_genres"""
        self.assertEqual(
            [
                Genre(name="rap", count=5),
                Genre(name="hip hop", count=5),
                Genre(name="underground hip hop", count=3),
                Genre(name="pop", count=3),
                Genre(name="alternative hip hop", count=2),
                Genre(name="pop rap", count=2),
            ],
            genres.get_genres(GenreQuery(aggregate=False), retriever),
        )
