"""Defines the Collection data model"""

from typing import Dict, Generic, List, TypeVar

from pydantic import BaseModel
from yaml import safe_load

from .artist import Artist
from .genre import Genre
from .rec import Rec
from .song import Song

T = TypeVar("T")  # pylint: disable=invalid-name


def load_headers() -> Dict[str, str]:
    """
    Loads item headers from the `item_headers.yaml` config file

    Returns
    -------
    content.collections: Dict[str, str]
        a mapping of content to the respective item headers
    """
    with open("./models/item_headers.yaml", encoding="utf-8") as handler:
        content = safe_load(handler)
        return content.get("collections", {})


COLLECTION_HEADERS = load_headers()


class Collection(BaseModel, Generic[T]):
    """
    A generic Collection type used to define a common model for a collection of
    content (i.e. artists, songs, etc.)
    """

    item_type: str
    """The name of the type of item in the collection - used for serialization"""

    items: List[T]
    """A list of content objects"""

    item_headers: List[str]
    """The names of the fields found on an object of type T"""

    count: int
    """The number of items in the collection"""

    @classmethod
    def from_list(cls, items: List[T]):
        """
        Creates a Collection[T] from a given List[T]

        Params
        ------
        items: List[T]
            a list of items of type T

        Returns
        -------
        collection: Collection[T]
            a collection whose items are of type T
        """
        item_type = ""
        headers = []
        match items:
            case [Artist(content=content), *_]:
                item_type = content
                headers = COLLECTION_HEADERS["artist"]

            case [Song(content=content), *_]:
                item_type = content
                headers = COLLECTION_HEADERS["song"]

            case [Genre(content=content), *_]:
                item_type = content
                headers = COLLECTION_HEADERS["genre"]

            case [Rec(content=content), *_]:
                item_type = content
                headers = COLLECTION_HEADERS["rec"]

            case _:
                raise TypeError(f"Unsupported item type {type(items[0])}")

        return Collection(
            item_type=item_type,
            items=items,
            item_headers=headers,
            count=len(items),
        )
