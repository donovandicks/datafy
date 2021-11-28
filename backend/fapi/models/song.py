"""Query models for Spotify songs"""

from typing import Optional

from pydantic import BaseModel, validator

from models.common import TimeRange


class SongQuery(BaseModel):
    """
    The type definition for available query params on the Songs resource.

    Members:
    - limit {Optional[int]}: The maximum number of songs to return in a single request
    - time_range {Optional[TimeRange]}: The time period from which to retrieve the requested data

    Inherits:
    - BaseModel: The pydantic base data model
    """

    limit: Optional[int]
    time_range: Optional[TimeRange]

    @validator("limit")
    def limit_is_positive(cls, lmt):  # pylint: disable=no-self-argument
        """Ensures that the limit passed is a positive value greater than 0"""
        if not lmt:
            return lmt

        if lmt <= 0:
            raise ValueError("limit must be at least 1")
        return lmt

    class Config:
        """Configuration for the QueryModel"""

        use_enum_values = True  # Allows passing enum values in query params


class Song(BaseModel):
    """The object model representing key elements of Spotify songs"""

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


class SongCollection(BaseModel):
    """The object model of the response body for the songs endpoint"""

    items: list[Song]
    """A list of song objects"""

    count: int
    """The number of items in the collection"""
