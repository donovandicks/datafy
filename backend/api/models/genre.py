"""Defines the structures of the data models used for interacting with the `/genres` route"""

from typing import Optional, Tuple

from pydantic import BaseModel

from .common import Query


class Genre(BaseModel):
    """The model for a `Genre` object"""

    content: str
    """The type of content - used for serialization"""

    name: str
    """The name of the genre"""

    count: int
    """The number of times the genre appeared"""

    @classmethod
    def from_tuple(cls, genre_tuple: Tuple[str, int]):
        """
        Creates a `Genre` object from a (name, count) tuple

        Params
        ------
        genre_tuple: Tuple[str, int]
            a (name, count) tuple

        Returns
        -------
        genre: Genre
            a `Genre` object with the data from the `genre_tuple`
        """
        return Genre(
            content="Genre",
            name=genre_tuple[0],
            count=genre_tuple[1],
        )


class GenreQuery(Query):
    """The query model for the `/genres` route"""

    aggregate: Optional[bool] = False
    """Whether to group genres by bin"""
