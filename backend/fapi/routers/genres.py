""""""

from operator import contains
from typing import Any, Callable, Dict, List, Optional, TypeAlias, TypeVar

from dependencies.spotify import init_spotify
from fastapi import APIRouter, Depends, HTTPException
from models.common import TimeRange
from models.genre import Genre, GenreQuery, GenreResponse

T = TypeVar("T")  # pylint: disable=invalid-name

GenreCount: TypeAlias = Dict[str, int]

CLIENT = init_spotify()

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


def get_genres_from_spotify(time_range: Optional[TimeRange], client=CLIENT) -> List[str]:
    """
    Retrieves a count of the occurrences of genres for the current users top artists

    Params
    ------
    time_range: Optional[TimeRange]
        the time_range parameter from which to retrieve results
    client: Spotify
        the api client used to connect to spotify

    Returns
    -------
    genre_detail: Dict[str, int]
        an object mapping a genre name to a count of its appearance

    Raises
    ------
    HTTPException(404)
        if the client is unable to retrieve any results
    """
    top_artists = client.current_user_top_artists(
        limit=50,
        time_range=time_range,
    )

    if not top_artists:
        raise HTTPException(404, "Top genres not found")

    genre_detail = []
    for item in top_artists["items"]:
        genre_detail.extend(item["genres"])

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


def get_genres(
    query: GenreQuery,
    retriever: Callable[[Optional[TimeRange]], List[str]],
) -> List[Genre]:
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
    genre_object = count_genres(retriever(query.time_range))

    if query.aggregate:
        genre_object = get_genre_aggregate(genre_object)

    genre_list = [
        Genre(name=name, count=count)
        for name, count in sorted(genre_object.items(), key=lambda genre: genre[1], reverse=True)
    ]

    return (
        genre_list[: query.limit] if (query.limit and query.limit < len(genre_list)) else genre_list
    )


@router.get("", response_model=GenreResponse)
async def get_top_genres(query: GenreQuery = Depends()) -> GenreResponse:
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
    return GenreResponse(items=get_genres(query, get_genres_from_spotify))
