"""Defines the logic for handling requests to the `/genres` route"""

from operator import contains
from typing import Any, Callable, Dict, List, TypeAlias, TypeVar

from dependencies.spotify import Client, SpotifyClient
from fastapi import APIRouter, Depends
from models.genre import Genre, GenreCollection, GenreQuery

T = TypeVar("T")  # pylint: disable=invalid-name

GenreCount: TypeAlias = Dict[str, int]

router = APIRouter(
    prefix="/genres",
    tags=["generes"],
)

GENRE_BINS = [
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
    "jazz",
    "classical",
]


def filter_dict(obj: Dict[str, T], opr: Callable[[str, Any], bool], query: Any) -> List[T]:
    """
    Uses an operator to compare dictionary keys against a query value to filter
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


def count_genres(genres: List[str]) -> GenreCount:
    """
    Iterates over artist objects, counting the occurrences of different genres as
    they appear

    Params
    ------
    artists: List[Dict]
        a list of artist objects returned from the api

    Returns
    -------
    genre_detail: Dict[str, int]
        a mapping of genre name to a count of its appearance
    """
    genre_detail = {}
    for genre in genres:
        genre_detail[genre] = genre_detail.setdefault(genre, 0) + 1

    return genre_detail


def get_genre_aggregate(genre_detail: GenreCount) -> GenreCount:
    """
    Aggregates detailed genre counts into broader, more general genres

    Params
    ------
    time_range: Optional[TimeRange]
        the time range from which to retrieve results

    Returns
    -------
    genre_aggregate: Dict[str, int]
        an object mapping a broad genre name to a count of its appearances
    """
    return {key: sum(filter_dict(genre_detail, contains, key)) for key in GENRE_BINS}


def get_genres(client: SpotifyClient) -> GenreCollection:
    """
    Retrieves a sorted list of Genre objects

    Params
    ------
    query: GenreQuery
        the query params used for the api client
    retriever: Callable[[Optional[TimeRange]], List[List[str]]]
        a function used to retrieve genres from spotify

    Returns
    -------
    genre_list: List[Genre]
        a list of genre objects
    """
    genre_object = count_genres(client.get_genres_from_spotify())

    if client.query.aggregate:
        genre_object = get_genre_aggregate(genre_object)

    genre_list = [
        Genre(name=name, count=count)
        for name, count in sorted(genre_object.items(), key=lambda genre: genre[1], reverse=True)
    ]

    items = (
        genre_list[: client.query.limit]
        if (client.query.limit and client.query.limit < len(genre_list))
        else genre_list
    )

    return GenreCollection(items=items, count=len(items))


@router.get("", response_model=GenreCollection)
async def get_top_genres(query: GenreQuery = Depends()) -> GenreCollection:
    """
    Retrieves the current users top genres

    Params
    ------
    query: GenreQuery
        the query params passed via the request

    Returns
    -------
    genres: GenreResponse
        the GenreResponse model with a list of genre objects
    """
    client = Client(query)
    return get_genres(client)
