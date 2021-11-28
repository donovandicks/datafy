"""Test Suite for the `/recs` route"""

from unittest import TestCase

from models.rec import Rec, RecCollection, RecQuery
from routers import recs

from .client_fixture import FakeClient


class RecsTest(TestCase):
    """Unit Tests for the `/recs` route"""

    def test_get_recs(self):
        """Test get_recs as expected"""
        self.assertEqual(
            RecCollection(
                items=[
                    Rec(song="Erase Your Social", artists=["Lil Uzi Vert"]),
                    Rec(song="Flex", artists=["Playboi Carti", "Leven Kali"]),
                    Rec(song="Self Care", artists=["Mac Miller"]),
                ],
                count=3,
            ),
            recs.get_recs(FakeClient(RecQuery())),
        )
