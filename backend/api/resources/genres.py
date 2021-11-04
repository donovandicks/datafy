"""The Genres resource"""

import operator
from typing import Any, Callable, Tuple, TypeVar

from flask import current_app as app
from flask_restful import NotFound, Resource
from models.genre_query import GenreModel
from pydantic_webargs import webargs

from resources.base import BaseService

T = TypeVar("T")

genre_bins = [
    "hip hop",
    "rap",
    "r&b",
    "metal",
    "rock",
]


def filter_dict(
    obj: dict[str, T], opr: Callable[[Any, Any], bool], query: Any
) -> list[T]:
    return [value for (key, value) in obj.items() if opr(key, query)]


class Genres(Resource, BaseService):
    """
    Defines the resource used for retrieving the genres
    """

    def _aggregate_genres(self, detail: dict[str, int]) -> dict[str, int]:
        app.logger.info("Aggregating genre counts for %i genres", len(detail.keys()))
        return {
            key: sum(filter_dict(detail, operator.contains, key)) for key in genre_bins
        }

    def _get_genres_for_artists(self, time_range: str) -> dict[str, int]:
        genre_count = {}
        top_artists = self.client.current_user_top_artists(
            limit=100,
            time_range=time_range,
        )

        if not top_artists:
            raise NotFound

        for artist in top_artists["items"]:
            for genre in artist["genres"]:
                genre_count[genre] = genre_count.setdefault(genre, 0) + 1

        return genre_count

    @webargs(query=GenreModel)
    def get(self, **kwargs) -> Tuple[dict, int, dict[str, str]]:
        """Retrieves the genres of all the top 100 pieces of content"""
        params = kwargs["query"]
        genre_count: dict[str, int] = {}

        if params["content"] == "artists":
            genre_count = self._get_genres_for_artists(params["time_range"])
            if params["aggregate"]:
                genre_count = self._aggregate_genres(genre_count)

        if params["content"] == "songs":
            # Songs do not appear to containt any genre information despite
            # documentation from Spotify. TODO: Look into efficient way to
            # query the genres for a given song - a cache or DB read may be
            # less intensive than a web api call
            raise NotImplementedError

        return (
            genre_count,
            200,
            {"Access-Control-Allow-Origin": "*"},
        )
