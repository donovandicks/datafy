"""Test Suite for the `/artists` route"""

from unittest import TestCase

from models.artist import Artist, ArtistQuery, ArtistResponse
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
            ArtistResponse(
                items=[
                    Artist(
                        id="ABC123", name="Jimbo", popularity=99, followers=1234567, genres=["folk"]
                    ),
                    Artist(
                        id="DEF456",
                        name="Jimothy",
                        popularity=97,
                        followers=1234234,
                        genres=["pop"],
                    ),
                ]
            ),
            artists.get_artists(FakeClient(ArtistQuery())),
        )

    def test_get_artist(self):
        """
        Tests that `get_artist_from_spotify` retrieves one artist
        """
        self.assertEqual(
            Artist(id="ABC123", name="Jimbo", popularity=99, followers=1234567, genres=["folk"]),
            artists.get_artist("ABC123", FakeClient(None)),
        )
