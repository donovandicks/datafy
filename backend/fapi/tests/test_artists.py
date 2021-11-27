"""Test Suite for the `/artists` route"""

from typing import Dict, List
from unittest import TestCase

from models.artist import Artist, ArtistQuery
from routers import artists


def retriever(_: ArtistQuery) -> List:
    """
    Test implementation of a retriever
    """
    return [
        {
            "id": "ABC123",
            "name": "Jimbo",
            "popularity": 99,
            "followers": {"total": 1234567},
            "other_field": "not_parsed",
        },
        {
            "id": "DEF456",
            "name": "Jimothy",
            "popularity": 97,
            "followers": {"total": 1234234},
            "other_field": "not_parsed",
        },
    ]


class Client:
    """
    Test implementation of the Spotipy client
    """

    def current_user_top_artists(self, limit, time_range) -> Dict[str, List]:
        """Test impl of Spotify.current_user_top_artists"""
        return {"items": retriever(ArtistQuery(limit=limit, time_range=time_range))}

    def artist(self, aid: str) -> Dict:
        """Test impl of Spotify.artist"""
        return {
            "id": aid,
            "name": "Jimbo",
            "popularity": 99,
            "followers": {"total": 1234567},
            "other_field": "not_parsed",
        }


class ArtistsTest(TestCase):
    """Unit tests for the `/artists` route"""

    def test_get_artists(self):
        """
        Tests that the `get_artists` function properly parses objects from
        the spotify api into `Artist` models
        """
        self.assertEqual(
            [
                Artist(id="ABC123", name="Jimbo", popularity=99, followers=1234567),
                Artist(id="DEF456", name="Jimothy", popularity=97, followers=1234234),
            ],
            artists.get_artists(ArtistQuery(), retriever),
        )

    def test_get_artists_from_spotify(self):
        """
        Tests that the `get_artists_from_spotify` function retrieves a list of
        items from Spotify
        """
        self.assertEqual(
            [
                {
                    "id": "ABC123",
                    "name": "Jimbo",
                    "popularity": 99,
                    "followers": {"total": 1234567},
                    "other_field": "not_parsed",
                },
                {
                    "id": "DEF456",
                    "name": "Jimothy",
                    "popularity": 97,
                    "followers": {"total": 1234234},
                    "other_field": "not_parsed",
                },
            ],
            artists.get_artists_from_spotify(
                ArtistQuery(),
                Client(),
            ),
        )

    def test_get_artist(self):
        """
        Tests that `get_artist_from_spotify` retrieves one artist
        """
        self.assertEqual(
            {
                "id": "ABC123",
                "name": "Jimbo",
                "popularity": 99,
                "followers": {"total": 1234567},
                "other_field": "not_parsed",
            },
            artists.get_artist_from_spotify("ABC123", Client()),
        )

    def test_parse_artist(self):
        """
        Tests that `parse_artist` produces a correct `Artist` model
        """
        self.assertEqual(
            Artist(id="ABC123", name="Jimbo", popularity=99, followers=1234567),
            artists.parse_artist(
                {
                    "id": "ABC123",
                    "name": "Jimbo",
                    "popularity": 99,
                    "followers": {"total": 1234567},
                    "other_field": "not_parsed",
                }
            ),
        )
