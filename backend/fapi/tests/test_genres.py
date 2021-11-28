"""Test Suite for the `/genres` route"""
from typing import Dict, List, Optional
from unittest import TestCase

from models.common import TimeRange
from models.genre import Genre, GenreQuery
from routers import genres


def retriever(_: Optional[TimeRange]) -> List[str]:
    """
    Test impl of a retriever
    """
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

    def test_count_genres(self):
        self.assertEqual(
            {
                "rap": 5,
                "hip hop": 5,
                "underground hip hop": 3,
                "alternative hip hop": 2,
                "pop": 3,
                "pop rap": 2,
            },
            genres.count_genres(
                [
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
            ),
        )

    def test_get_genres_from_spotify(self):
        self.assertEqual(
            [
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
            ],
            genres.get_genres_from_spotify(None, Client()),
        )

    def test_get_genre_agg(self):
        """Tests get_genres with aggregation"""
        self.assertEqual(
            [
                Genre(name="hip hop", count=10),
                Genre(name="rap", count=7),
                Genre(name="pop", count=5),
                Genre(name="r&b", count=0),
                Genre(name="metal", count=0),
                Genre(name="rock", count=0),
                Genre(name="indie", count=0),
                Genre(name="soul", count=0),
                Genre(name="folk", count=0),
                Genre(name="electronic", count=0),
                Genre(name="country", count=0),
                Genre(name="jazz", count=0),
                Genre(name="classical", count=0),
            ],
            genres.get_genres(GenreQuery(aggregate=True), retriever),
        )

    def test_get_genre_detail(self):
        """Tests get_genres without aggregation"""
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
