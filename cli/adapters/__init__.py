"""Initializes the Adapters module"""

from typing import Type

from adapters.artists import ArtistsAdapter
from adapters.base import Adapter
from adapters.genres import GenresAdapter
from adapters.songs import SongsAdapter

ADAPTERS: dict[str, Type[Adapter]] = {
    "songs": SongsAdapter,
    "artists": ArtistsAdapter,
    "genres": GenresAdapter,
}
