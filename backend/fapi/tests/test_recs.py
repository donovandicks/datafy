"""Test Suite for the `/recs` route"""

from typing import List
from unittest import TestCase

from models.rec import Rec, RecQuery
from routers import recs


def retriever(_: RecQuery) -> List:
    """Test impl of a retriever"""
    return [
        {"name": "Erase Your Social", "artists": [{"name": "Lil Uzi Vert"}]},
        {"name": "Flex", "artists": [{"name": "Playboi Carti"}, {"name": "Leven Kali"}]},
        {"name": "Self Care", "artists": [{"name": "Mac Miller"}]},
    ]


class Client:
    """Test impl of the Spotipy client"""

    # pylint: disable=unused-argument
    def recommendations(self, seed_artists, seed_genres, seed_tracks, limit):
        """Test impl of Spotipy.recommendations"""
        return {
            "tracks": [
                {"name": "Erase Your Social", "artists": [{"name": "Lil Uzi Vert"}]},
                {"name": "Flex", "artists": [{"name": "Playboi Carti"}, {"name": "Leven Kali"}]},
                {"name": "Self Care", "artists": [{"name": "Mac Miller"}]},
            ]
        }


class RecsTest(TestCase):
    """Unit Tests for the `/recs` route"""

    def test_get_recs(self):
        """Test get_recs as expected"""
        self.assertEqual(
            [
                Rec(song="Erase Your Social", artists=["Lil Uzi Vert"]),
                Rec(song="Flex", artists=["Playboi Carti", "Leven Kali"]),
                Rec(song="Self Care", artists=["Mac Miller"]),
            ],
            recs.get_recs(RecQuery(), retriever),
        )

    def test_get_recommendations_from_spotify(self):
        """Test get_recommendations_from_spotify as expected"""
        self.assertEqual(
            [
                {"name": "Erase Your Social", "artists": [{"name": "Lil Uzi Vert"}]},
                {"name": "Flex", "artists": [{"name": "Playboi Carti"}, {"name": "Leven Kali"}]},
                {"name": "Self Care", "artists": [{"name": "Mac Miller"}]},
            ],
            recs.get_recommendations_from_spotify(RecQuery(), Client()),
        )
