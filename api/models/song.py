"""Query models for Spotify songs"""

from typing import Dict

from pydantic import BaseModel

from models.common import Query


class SongQuery(Query):
    """The query model for the `/songs` route"""


class Song(BaseModel):
    """The object model representing key elements of Spotify songs"""

    content: str
    """The type of content - used for serialization"""

    id: str
    """The Spotify ID of the song"""

    name: str
    """The name of the song"""

    artists: list[str]
    """The artist(s) who perform the song"""

    popularity: int
    """The popularity of the song from 0 to 100"""

    album: str
    """The album the song is from"""

    release_date: str
    """The date the album was first released"""

    @classmethod
    def from_dict(cls, song: Dict):
        """
        Converts a dictionary into a `Song` object

        Params
        ------
        song: Dict
            a song object returned from Spotify

        Returns
        -------
        song: Song
            a `Song` object with the data elements from the input `song`
        """
        return Song(
            content="Song",
            id=song["id"],
            name=song["name"],
            artists=[artist["name"] for artist in song["artists"]],
            popularity=song["popularity"],
            album=song["album"]["name"],
            release_date=song["album"]["release_date"],
        )
