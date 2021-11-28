"""Defines the logic for handling requests to the `/songs` route"""

from dependencies.spotify import Client, SpotifyClient
from fastapi import APIRouter, Depends
from models.song import Song, SongCollection, SongQuery

router = APIRouter(prefix="/songs", tags=["songs"])


def get_song(song_id: str, client: SpotifyClient) -> Song:
    """
    Retrieves an individual song from Spotify formatted as a `Song`

    Params
    ------
    artist_id: str
        the Spotify artist ID, URI, or URL used to identify the song
    client: SpotifyClient
        a api client object used to connect to Spotify

    Returns
    -------
    artist: Song
        an object containing data about a song
    """

    return Song.from_dict(client.get_song_from_spotify(song_id))


def get_songs(client: SpotifyClient) -> SongCollection:
    """
    Retrieves a list of songs from Spotify formatted as an `SongCollection`

    Params
    ------
    client: SpotifyClient
        a api client object used to connect to Spotify

    Returns
    -------
    artists: SongCollection
        an object containing a list of songs and a count of songs retrieved
    """
    songs = [Song.from_dict(song) for song in client.get_songs_from_spotify()]
    return SongCollection(items=songs, count=len(songs))


@router.get("", response_model=SongCollection)
async def get_top_songs(query: SongQuery = Depends()) -> SongCollection:
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
    client = Client(query)
    return get_songs(client)


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
    client = Client(SongQuery())
    return get_song(song_id, client)
