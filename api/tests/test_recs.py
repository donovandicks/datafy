"""Test Suite for the `/recs` route"""

from unittest import TestCase

from models.collection import Collection
from models.rec import Rec, RecQuery
from routes import recs

from .client_fixture import FakeClient


class RecsTest(TestCase):
    """Unit Tests for the `/recs` route"""

    def test_get_recs(self):
        """Test get_recs as expected"""
        self.assertEqual(
            Collection(
                item_type="Recommendation",
                items=[
                    Rec(
                        content="Recommendation",
                        song="Erase Your Social",
                        artists=["Lil Uzi Vert"],
                    ),
                    Rec(
                        content="Recommendation",
                        song="Flex",
                        artists=["Playboi Carti", "Leven Kali"],
                    ),
                    Rec(
                        content="Recommendation",
                        song="Self Care",
                        artists=["Mac Miller"],
                    ),
                ],
                item_headers=["Song", "Artist"],
                count=3,
            ),
            recs.get_recs(FakeClient(RecQuery())),
        )
