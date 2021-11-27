"""Defines the logic for handling requests to the `/songs` route"""
from typing import Callable, Dict, List

from dependencies.spotify import CLIENT
from fastapi import APIRouter, Depends, HTTPException
from models.song import Song, SongQuery, SongResponse

router = APIRouter(prefix="/songs", tags=["songs"])


def parse_song(song: Dict) -> Song:
    """
    Parses an object returned by the api into a `Song` model

    Params
    ------
    song: Dict
        a song object returned by the api

    Returns
    -------
    song: Song
        the parsed song model
    """
    return Song(
        id=song["id"],
        name=song["name"],
        artists=[artist["name"] for artist in song["artists"]],
        popularity=song["popularity"],
        album=song["album"]["name"],
        release_date=song["album"]["release_date"],
    )


def get_song_from_spotify(song_id: str, client=CLIENT) -> Dict:
    """
    Retrieves a single song from spotify

    Params
    ------
    song_id: str
        the spotify ID, URI, or URL for the song
    client: [Spotify]
        the api client used to connect to spotify

    Raises
    ------
    HTTPException(404)
        if the song is not found
    """
    song = client.track(song_id)

    if not song:
        raise HTTPException(404, "Song not found")

    return song


def get_songs_from_spotify(query: SongQuery, client=CLIENT) -> List[Dict]:
    """
    Retrieves the current users top songs from spotify

    Params
    ------
    query: SongQuery
        the query model for the `/songs` route
    client: [Spotify]
        the api client used to connect to spotify

    Returns
    -------
    top_songs: List[Dict]
        a  list of spotify song objects from the api

    Raises
    ------
    HTTPException(404)
        if no top songs are found
    """
    top_songs = client.current_user_top_tracks(limit=query.limit, time_range=query.time_range)

    if not top_songs:
        raise HTTPException(404, "Top songs not found")

    return top_songs["items"]


def get_songs(query: SongQuery, retriever: Callable[[SongQuery], List[Dict]]) -> List[Song]:
    """
    Parses songs returned from a retriever function into a list of `Song` models.

    Params
    ------
    query: SongQuery
        the query params passed in by the user
    retriever: fn(SongQuery) -> List[Dict]
        a function that takes a `SongQuery` argument and returns a list of song
        objects

    Returns
    -------
    songs: List[Song]
        a list of parsed `Song` models
    """
    return [parse_song(song) for song in retriever(query)]


@router.get("", response_model=SongResponse)
async def get_top_songs(query: SongQuery = Depends()) -> SongResponse:
    """
    Retrieves the current users top songs from the spotify api

    Params
    ------
    query: SongQuery
        the query params included in the endpoint URL

    Returns
    -------
    songs: SongResponse
        the formatted songs retrieved from the spotify api
    """
    return SongResponse(
        items=get_songs(
            query,
            get_songs_from_spotify,
        )
    )


@router.get("/{song_id}", response_model=Song)
async def get_one_song(song_id: str) -> Song:
    """
    Retrieves a single song from spotify

    Params
    ------
    song_id: str
        the song ID, URI, or URL

    Returns
    -------
    song: Song
        a song model constructed from the spotify response object
    """
    return parse_song(get_song_from_spotify(song_id))
