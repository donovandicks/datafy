"""The Genres resource"""

import operator
from typing import Any, Callable, Tuple, TypeVar

from flask import current_app as app
from flask_restful import NotFound, Resource
from models.genre_query import GenreModel
from pydantic_webargs import webargs

from resources.base import BaseService

T = TypeVar("T")  # pylint: disable=invalid-name

# TODO: Support an 'other' category that aggregates all other genres that don't
# match below
genre_bins = [
    "hip hop",
    "rap",
    "r&b",
    "metal",
    "rock",
    "pop",
    "indie",
    "soul",
    "folk",
    "electronic",
    "country",
]


def filter_dict(
    obj: dict[str, T], opr: Callable[[Any, Any], bool], query: Any
) -> list[T]:
    """Uses an operator to compare dictionary keys against a query value to filter
    the dictionary and retrieve the values for the matching keys

    Params
    ------
    obj: dict[str, T]
        the dictionary to filter on
    opr: Callable[[Any, Any], bool]
        an operator function that takes any two arguments and returns a boolean
    query: Any
        the value used to filter keys

    Returns
    -------
    values: list[T]
        a list of all the values for the keys that matched the given query
    """
    return [value for (key, value) in obj.items() if opr(key, query)]


class Genres(Resource, BaseService):
    """
    Defines the resource used for retrieving the genres
    """

    def _aggregate_genres(self, detail: dict[str, int]) -> dict[str, int]:
        """Aggregates a detailed genre report into a high-level report with
        broader genres

        Params
        ------
        detail: dict[str, int]
            an object containing a mapping of genres to counts

        Returns
        -------
        aggregate: dict[str, int]
            an object mapping broader genres to aggregated counts from subgenres
        """
        app.logger.info("Aggregating genre counts for %i genres", len(detail.keys()))
        return {
            key: sum(filter_dict(detail, operator.contains, key)) for key in genre_bins
        }

    def _get_genres_for_artists(self, time_range: str) -> dict[str, int]:
        """Generates a mapping from subgenre to count of appearance for all genres
        associated with the current users top 100 artists

        Params
        ------
        time_range: str
            a Spotify API support time_range [short_term|medium_term|long_term]

        Returns
        -------
        genre_count: dict[str, int]
            an object mapping subgenres to a count of their appearances
        """
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

    def __sort_genres_by_count(self, genre_count) -> dict[str, int]:
        """Sorts the dictionary of genres and song count descending by song count.

        Parameters
        ----------
        genre_count : dict[str, int]
            The dictionary of genre to the number of songs in that genre

        Returns
        -------
        dict[str, int]
            The sorted dictionary.

        """
        # creates a tuple of the original dict, sorted descending by count, then creates a new dict
        sorted_genres = dict(sorted(genre_count.items(), key=lambda x: x[1], reverse=True))
        return sorted_genres

    @webargs(query=GenreModel)
    def get(self, **kwargs) -> Tuple[dict[str, dict], int, dict[str, str]]:
        """Retrieves the genres of all the top 100 pieces of content"""
        params = kwargs["query"]
        genre_count: dict[str, int] = {}

        match params["content"]:
            case "artists" | None:
                genre_count = self._get_genres_for_artists(params["time_range"])
                if params["aggregate"]:
                    genre_count = self._aggregate_genres(genre_count)

            case "songs":
                # Songs do not appear to containt any genre information despite
                # documentation from Spotify. TODO: Look into efficient way to
                # query the genres for a given song - a cache or DB read may be
                # less intensive than a web api call
                raise NotImplementedError

            case _:
                raise Exception("Content type not supported")

        sorted_genre_count = self.__sort_genres_by_count(genre_count)

        num_items = len(sorted_genre_count)
        if params["limit"] and params["limit"] < num_items:
            num_items = params["limit"]

        return (
            {"items": dict(list(sorted_genre_count.items())[:num_items])},
            200,
            {"Access-Control-Allow-Origin": "*"},
        )
