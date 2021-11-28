"""Test Suite for the `/genres` route"""
from unittest import TestCase

from models.genre import Genre, GenreCollection, GenreQuery
from routers import genres

from .client_fixture import FakeClient


class GenresTest(TestCase):
    """Unit tests for the genres logic"""

    def test_count_genres(self):
        """Tests count_genres"""
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

    def test_get_genre_agg(self):
        """Tests get_genres with aggregation"""
        self.assertEqual(
            GenreCollection(
                items=[
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
                count=13,
            ),
            genres.get_genres(FakeClient(GenreQuery(aggregate=True))),
        )

    def test_get_genre_detail(self):
        """Tests get_genres without aggregation"""
        self.assertEqual(
            GenreCollection(
                items=[
                    Genre(name="rap", count=5),
                    Genre(name="hip hop", count=5),
                    Genre(name="underground hip hop", count=3),
                    Genre(name="pop", count=3),
                    Genre(name="alternative hip hop", count=2),
                    Genre(name="pop rap", count=2),
                ],
                count=6,
            ),
            genres.get_genres(FakeClient(GenreQuery(aggregate=False))),
        )
