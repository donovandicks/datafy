"""Defines the logic for handling requests to the `/artists` route"""
from typing import Any, Callable, Dict, List

from dependencies.spotify import CLIENT
from fastapi import APIRouter, Depends, HTTPException
from models.artist import Artist, ArtistQuery, ArtistResponse

router = APIRouter(
    prefix="/artists",
    tags=["artists"],
)


def get_artist_from_spotify(artist_id: str, client=CLIENT) -> Dict[str, Any]:
    """
    Retrieves a single artist from spotify

    Params
    ------
    artist_id: str
        the spotify ID, URI, or URL of the artist

    Returns
    -------
    artist: Dict
        the artist object
    client: [Spotify]
        the api client used to connect to spotify

    Raises
    ------
    HTTPException(404)
        if no artist is found for the ID
    """

    artist = client.artist(artist_id)

    if not artist:
        raise HTTPException(404, f"Artist {artist_id} not found")

    return artist


def get_artists_from_spotify(query: ArtistQuery, client=CLIENT) -> List:
    """
    Retrieves the current users top artists from spotify

    Params
    ------
    query: ArtistQuery
        the query model for the `/artists` route
    client: [Spotify]
        the api client used to connect to spotify

    Returns
    -------
    top_artists: List
        a list of spotify artist objects retrieved from the api

    Raises
    ------
    HTTPException(404)
        if no top artists are found for the current user
    """
    top_artists = client.current_user_top_artists(
        limit=query.limit,
        time_range=query.time_range,
    )

    if not top_artists:
        raise HTTPException(404, "Top artists not found")

    return top_artists["items"]


def get_artists(query: ArtistQuery, retriever: Callable[[ArtistQuery], List[Dict]]) -> List[Artist]:
    """
    Parses songs returned from a retriever function into a list of `Artist` models.

    Params
    ------
    query: ArtistQuery
        the query model for the `/artists` route
    retriever: Callable[[ArtistQuery], List[Dict]]
        a function that takes a `ArtistQuery` argument and returns a list of artist
        objects

    Returns
    -------
    artists: List[Artist]
        a list of parsed `Artist` models
    """
    return [Artist.from_dict(item) for item in retriever(query)]


@router.get("", response_model=ArtistResponse)
async def get_top_artists(query: ArtistQuery = Depends()) -> ArtistResponse:
    """
    Retrieves the current users top artists from the spotify api

    Params
    ------
    query: ArtistQuery
        the query params included in the endpoint URL

    Returns
    -------
    artists: ArtistResponse
        the formatted artists retrieved from the spotify api
    """
    return ArtistResponse(items=get_artists(query, get_artists_from_spotify))


@router.get("/{artist_id}", response_model=Artist)
async def get_one_artist(artist_id: str) -> Artist:
    """
    Retrieves a single artist from spotify

    Params
    ------
    artist_id: str
        the artist ID, URI, or URL

    Returns
    -------
    artist: Artist
        an artist model constructed from the spotify response object
    """
    return Artist.from_dict(get_artist_from_spotify(artist_id))