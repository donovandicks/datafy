"""Defines the structure of the data returned by the artists response"""

from pydantic import BaseModel


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

    items: list[Artist]
    """The list of all Artists retrieved from Spotify"""
