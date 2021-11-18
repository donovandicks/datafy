"""The Genres resource"""

import operator
from typing import Any, Callable, TypeVar

from flask import current_app as app
from flask.wrappers import Response
from flask_restful import NotFound, Resource
from models.genre_query import GenreQuery
from models.genre_response import GenreResponse
from pydantic_webargs import webargs

from resources.base import BaseService

T = TypeVar("T")  # pylint: disable=invalid-name

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


def filter_dict(obj: dict[str, T], opr: Callable[[str, Any], bool], query: Any) -> list[T]:
    """Uses an operator to compare dictionary keys against a query value to filter
    the dictionary and retrieve the values for the matching keys

    Params
    ------
    obj: dict[str, T]
        the dictionary to filter on
    opr: Callable[[str, Any], bool]
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

    def __init__(self) -> None:
        self.genre_detail: dict[str, int] = {}
        self.genre_aggregate: dict[str, int] = {}
        self.query: GenreQuery = GenreQuery()
        super().__init__()

    def __aggregate_genres(self):
        """Aggregates a detailed genre report into a high-level report with
        broader genres

        Params
        ------
        detail: dict[str, int]
            an object containing a mapping of genres to counts
        """
        app.logger.info("Aggregating genre counts for %i genres", len(self.genre_detail))
        self.genre_aggregate = {
            key: sum(filter_dict(self.genre_detail, operator.contains, key)) for key in genre_bins
        }

    def __get_genres_for_artists(self):
        """Generates a mapping from subgenre to count of appearance for all genres
        associated with the current users top 100 artists

        Params
        ------
        time_range: str
            a Spotify API support time_range [short_term|medium_term|long_term]
        """
        top_artists = self.client.current_user_top_artists(
            limit=50,
            time_range=self.query.time_range,
        )

        if not top_artists:
            raise NotFound

        for artist in top_artists["items"]:
            for genre in artist["genres"]:
                self.genre_detail[genre] = self.genre_detail.setdefault(genre, 0) + 1

    def __sort_genres_by_count(self) -> dict[str, int]:
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
        genre_count = self.genre_aggregate if self.query.aggregate else self.genre_detail

        return dict(sorted(genre_count.items(), key=lambda x: x[1], reverse=True))

    def __count_genres(self):
        """Counts the occurrences of genres for all artists and aggregates the
        count if the aggregate query param is passed
        """
        self.__get_genres_for_artists()

        if self.query.aggregate:
            self.__aggregate_genres()

    def __get_response_body(self) -> GenreResponse:
        """Retrieves the body data for the response object

        Returns
        -------
        GenreResponse
            the data model object containing a sorted dictionary of genre counts
        """
        self.__count_genres()
        sorted_genre_count = self.__sort_genres_by_count()

        num_items = len(sorted_genre_count)
        if self.query.limit and self.query.limit < num_items:
            # Use the query limit if it is within valid bounds
            num_items = self.query.limit

        # Slices the dictionary to retrieve the first num_items of genres
        return GenreResponse(items=dict(list(sorted_genre_count.items())[:num_items]))

    @webargs(query=GenreQuery)
    def get(self, **kwargs) -> Response:
        """Retrieves the genres of all the top 100 pieces of content"""
        self.query = GenreQuery(**kwargs["query"])

        return Response(
            response=self.__get_response_body().json(),
            status=200,
            headers={"Access-Control-Allow-Origin": "*"},
            content_type="application/json",
        )
