"""Defines the structure of the data returned by the songs response"""

from pydantic import BaseModel


class Song(BaseModel):
    """The object model representing key elements of Spotify songs"""

    id: str
    """The Spotify ID of the song"""

    name: str
    """The name of the song"""

    artists: str | list[str]
    """The artist(s) who perform the song"""

    popularity: int
    """The popularity of the song from 0 to 100"""

    album: str
    """The album the song is from"""

    release_date: str
    """The date the album was first released"""


class SongResponse(BaseModel):
    """The object model of the response body for the songs endpoint"""

    items: list[Song]
