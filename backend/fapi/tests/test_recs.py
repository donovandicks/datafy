"""Test Suite for the `/recs` route"""

from typing import Dict, List
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
    def recommendations(self, seed_artists, seed_genres, seed_tracks, limit):
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
        self.assertEqual(
            [
                Rec(song="Erase Your Social", artists=["Lil Uzi Vert"]),
                Rec(song="Flex", artists=["Playboi Carti", "Leven Kali"]),
                Rec(song="Self Care", artists=["Mac Miller"]),
            ],
            recs.get_recs(RecQuery(), retriever),
        )

    def test_get_recommendations_from_spotify(self):
        self.assertEqual(
            [
                {"name": "Erase Your Social", "artists": [{"name": "Lil Uzi Vert"}]},
                {"name": "Flex", "artists": [{"name": "Playboi Carti"}, {"name": "Leven Kali"}]},
                {"name": "Self Care", "artists": [{"name": "Mac Miller"}]},
            ],
            recs.get_recommendations_from_spotify(RecQuery(), Client()),
        )
