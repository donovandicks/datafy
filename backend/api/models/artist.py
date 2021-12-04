"""Defines the structures of the data models used for interacting with the `/artists` route"""
from typing import Dict, List

from pydantic import BaseModel

from .common import Query


class ArtistQuery(Query):
    """The query model for the `/artists` route"""


class Artist(BaseModel):
    """
    The object model representing key elements of a Spotify artist
    """

    content: str

    id: str
    """The Spotify ID of the artist"""

    name: str
    """The name of the artist"""

    popularity: int
    "The popularity of the artist from 0 to 100"

    followers: int
    """The total number of followers that the artist has"""

    genres: List[str]
    """The genres for the artists music"""

    @classmethod
    def from_dict(cls, obj: Dict):
        """Converts a dictionary to an `Artist` object"""
        return Artist(
            content="Artist",
            id=obj["id"],
            name=obj["name"],
            popularity=obj["popularity"],
            followers=obj["followers"]["total"],
            genres=obj["genres"],
        )
