"""Test Suite for the `/songs` route"""

from unittest import TestCase

from models.collection import Collection
from models.song import Song, SongQuery
from routes import songs

from .client_fixture import FakeClient


class SongsTest(TestCase):
    """Unit tests for songs logic"""

    def test_get_songs(self):
        """Tests that `get_songs` parses objects into a list of `Song` models"""
        self.assertEqual(
            Collection(
                item_type="Song",
                items=[
                    Song(
                        content="Song",
                        id="ABC123",
                        name="Love Song",
                        artists=["Wesley"],
                        popularity=99,
                        album="The Princess Bride",
                        release_date="1987-09-07",
                        other_field="not_parsed",
                    ),
                    Song(
                        content="Song",
                        id="DEF456",
                        name="Pirate Song",
                        artists=["Jack Sparrow"],
                        popularity=95,
                        album="Pirates of the Carribean",
                        release_date="2001-05-15",
                        other_field="not_parsed",
                    ),
                ],
                item_headers=[
                    "Rank",
                    "Song",
                    "Artists",
                    "Popularity",
                    "Release Date",
                    "ID",
                ],
                count=2,
            ),
            songs.get_songs(FakeClient(SongQuery())),
        )

    def test_get_song(self):
        """Tests that `get_song_from_spotify` retrieves a single song from the client"""
        self.assertEqual(
            Song(
                content="Song",
                id="ABC123",
                name="Love Song",
                artists=["Wesley"],
                popularity=99,
                album="The Princess Bride",
                release_date="1987-09-07",
                other_field="not_parsed",
            ),
            songs.get_song("ABC123", FakeClient(SongQuery())),
        )
