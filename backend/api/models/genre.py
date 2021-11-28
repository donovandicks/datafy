"""Defines the structures of the data models used for interacting with the `/genres` route"""

from typing import List

from pydantic import BaseModel

from .common import Query


class Genre(BaseModel):
    """The model for a `Genre` object"""

    name: str
    count: int


class GenreQuery(Query):
    """The query model for the `/genres` route"""

    aggregate: bool
    """Whether to group genres by bin"""


class GenreCollection(BaseModel):
    """The object model of the response body for the `/genres` route"""

    items: List[Genre]
    """A list of all genres retrieved from Spotify"""

    count: int
    """The number of items in the collection"""
