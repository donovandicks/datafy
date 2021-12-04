"""Test Suite for the `/artists` route"""

from unittest import TestCase

from models.artist import Artist, ArtistQuery
from models.collection import Collection
from routers import artists

from .client_fixture import FakeClient


class ArtistsTest(TestCase):
    """Unit tests for the artists logic"""

    def test_get_artists(self):
        """
        Tests that the `get_artists` function properly parses objects from
        the spotify api into `Artist` models
        """
        self.assertEqual(
            Collection(
                item_type="Artist",
                items=[
                    Artist(
                        content="Artist",
                        id="ABC123",
                        name="Jimbo",
                        popularity=99,
                        followers=1234567,
                        genres=["folk"],
                    ),
                    Artist(
                        content="Artist",
                        id="DEF456",
                        name="Jimothy",
                        popularity=97,
                        followers=1234234,
                        genres=["pop"],
                    ),
                ],
                item_headers=["Rank", "Artist", "Popularity", "Followers", "Genres", "ID"],
                count=2,
            ),
            artists.get_artists(FakeClient(ArtistQuery())),
        )

    def test_get_artist(self):
        """
        Tests that `get_artist_from_spotify` retrieves one artist
        """
        self.assertEqual(
            Artist(
                content="Artist",
                id="ABC123",
                name="Jimbo",
                popularity=99,
                followers=1234567,
                genres=["folk"],
            ),
            artists.get_artist("ABC123", FakeClient(None)),
        )
