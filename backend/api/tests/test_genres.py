"""Test Suite for the `/genres` route"""
from unittest import TestCase

from models.collection import Collection
from models.genre import Genre, GenreQuery
from routers import genres

from .client_fixture import FakeClient


class GenresTest(TestCase):
    """Unit tests for the genres logic"""

    def test_get_genre_agg(self):
        """Tests get_genres with aggregation"""
        self.assertEqual(
            Collection(
                item_type="Genre",
                items=[
                    Genre(content="Genre", name="hip hop", count=10),
                    Genre(content="Genre", name="rap", count=7),
                    Genre(content="Genre", name="pop", count=5),
                    Genre(content="Genre", name="r&b", count=0),
                    Genre(content="Genre", name="metal", count=0),
                    Genre(content="Genre", name="rock", count=0),
                    Genre(content="Genre", name="indie", count=0),
                    Genre(content="Genre", name="soul", count=0),
                    Genre(content="Genre", name="folk", count=0),
                    Genre(content="Genre", name="electronic", count=0),
                    Genre(content="Genre", name="country", count=0),
                    Genre(content="Genre", name="jazz", count=0),
                    Genre(content="Genre", name="classical", count=0),
                ],
                item_headers=["Rank", "Genre", "Count"],
                count=13,
            ),
            genres.get_genres(FakeClient(GenreQuery(aggregate=True))),
        )

    def test_get_genre_detail(self):
        """Tests get_genres without aggregation"""
        self.assertEqual(
            Collection(
                item_type="Genre",
                items=[
                    Genre(content="Genre", name="rap", count=5),
                    Genre(content="Genre", name="hip hop", count=5),
                    Genre(content="Genre", name="underground hip hop", count=3),
                    Genre(content="Genre", name="pop", count=3),
                    Genre(content="Genre", name="alternative hip hop", count=2),
                    Genre(content="Genre", name="pop rap", count=2),
                ],
                item_headers=["Rank", "Genre", "Count"],
                count=6,
            ),
            genres.get_genres(FakeClient(GenreQuery(aggregate=False))),
        )
