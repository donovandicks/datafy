"""Defines the structures of the data models used for interacting with the `/artists` route"""
from typing import List, Optional

from pydantic import BaseModel, validator

from models.common import TimeRange


class ArtistQuery(BaseModel):
    """The query model for the Artists resource"""

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
        """Defines the configuration for the query model"""

        use_enum_values = True


class Artist(BaseModel):
    """
    The object model representing key elements of a Spotify artist
    """

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


class ArtistResponse(BaseModel):
    """
    The object model of the response body for the artists endpoint

    ```
    items: [
        {
            id: string,
            name: string,
            popularity: int,
            followers: int,
        }
    ]
    ```
    """

    items: List[Artist]
    """The list of all Artists retrieved from Spotify"""
