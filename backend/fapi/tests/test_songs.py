"""Test Suite for the `/songs` route"""

from typing import Dict, List
from unittest import TestCase

from models.song import Song, SongQuery
from routers import songs


def retriever(_: SongQuery) -> List:
    """
    Test impl of a retriever
    """
    return [
        {
            "id": "ABC123",
            "name": "Love Song",
            "artists": [{"name": "Wesley"}],
            "popularity": 99,
            "album": {
                "name": "The Princess Bride",
                "release_date": "1987-09-07",
            },
            "other_field": "not_parsed",
        },
        {
            "id": "DEF456",
            "name": "Pirate Song",
            "artists": [{"name": "Jack Sparrow"}],
            "popularity": 95,
            "album": {
                "name": "Pirates of the Carribean",
                "release_date": "2001-05-15",
            },
            "other_field": "not_parsed",
        },
    ]


class Client:
    """Test impl of a Spotify client"""

    def current_user_top_tracks(self, limit, time_range) -> Dict[str, list]:
        """Test impl of Spotify.current_user_top_tracks"""
        return {"items": retriever(SongQuery(limit=limit, time_range=time_range))}

    def track(self, sid: str) -> Dict:
        """Test impl of Spotify.track"""
        return {
            "id": sid,
            "name": "Love Song",
            "artists": [{"name": "Wesley"}],
            "popularity": 99,
            "album": {"name": "The Princess Bride", "release_date": "1987-09-07"},
            "other_field": "not_parsed",
        }


class SongsTest(TestCase):
    """Unit tests for songs logic"""

    def test_get_songs(self):
        """Tests that `get_songs` parses objects into a list of `Song` models"""
        self.assertEqual(
            [
                Song(
                    id="ABC123",
                    name="Love Song",
                    artists=["Wesley"],
                    popularity=99,
                    album="The Princess Bride",
                    release_date="1987-09-07",
                    other_field="not_parsed",
                ),
                Song(
                    id="DEF456",
                    name="Pirate Song",
                    artists=["Jack Sparrow"],
                    popularity=95,
                    album="Pirates of the Carribean",
                    release_date="2001-05-15",
                    other_field="not_parsed",
                ),
            ],
            songs.get_songs(SongQuery(), retriever),
        )

    def test_get_songs_from_spotify(self):
        """Tests that `get_songs_from_spotify` retrieves a list of songs from the client"""
        self.assertEqual(
            [
                {
                    "id": "ABC123",
                    "name": "Love Song",
                    "artists": [{"name": "Wesley"}],
                    "popularity": 99,
                    "album": {"name": "The Princess Bride", "release_date": "1987-09-07"},
                    "other_field": "not_parsed",
                },
                {
                    "id": "DEF456",
                    "name": "Pirate Song",
                    "artists": [{"name": "Jack Sparrow"}],
                    "popularity": 95,
                    "album": {"name": "Pirates of the Carribean", "release_date": "2001-05-15"},
                    "other_field": "not_parsed",
                },
            ],
            songs.get_songs_from_spotify(SongQuery(), Client()),
        )

    def test_get_song(self):
        """Tests that `get_song_from_spotify` retrieves a single song from the client"""
        self.assertEqual(
            {
                "id": "ABC123",
                "name": "Love Song",
                "artists": [{"name": "Wesley"}],
                "popularity": 99,
                "album": {"name": "The Princess Bride", "release_date": "1987-09-07"},
                "other_field": "not_parsed",
            },
            songs.get_song_from_spotify("ABC123", Client()),
        )

    def test_parse_song(self):
        """Tests that `parse_song` produces a correct `Song` model"""
        self.assertEqual(
            Song(
                id="ABC123",
                name="Love Song",
                artists=["Wesley"],
                popularity=99,
                album="The Princess Bride",
                release_date="1987-09-07",
                other_field="not_parsed",
            ),
            songs.parse_song(
                {
                    "id": "ABC123",
                    "name": "Love Song",
                    "artists": [{"name": "Wesley"}],
                    "popularity": 99,
                    "album": {"name": "The Princess Bride", "release_date": "1987-09-07"},
                    "other_field": "not_parsed",
                }
            ),
        )
