"""Defines the logic for handling requests to the `/artists` route"""
from dependencies.spotify import Client, SpotifyClient
from fastapi import APIRouter, Depends
from models.artist import Artist, ArtistCollection, ArtistQuery

router = APIRouter(
    prefix="/artists",
    tags=["artists"],
)


def get_artist(artist_id: str, client: SpotifyClient) -> Artist:
    """
    Retrieves an individual artist from Spotify formatted as an `Artist`

    Params
    ------
    artist_id: str
        the Spotify artist ID, URI, or URL used to identify the artist
    client: SpotifyClient
        a api client object used to connect to Spotify

    Returns
    -------
    artist: Artist
        an object containing data about an artist
    """
    return Artist.from_dict(client.get_artist_from_spotify(artist_id))


def get_artists(client: SpotifyClient) -> ArtistCollection:
    """
    Retrieves a list of artists from Spotify formatted as an `ArtistResponse`

    Params
    ------
    client: SpotifyClient
        a api client object used to connect to Spotify

    Returns
    -------
    artists: ArtistResponse
        an object containing a list of artists
    """
    artists = [Artist.from_dict(item) for item in client.get_artists_from_spotify()]
    return ArtistCollection(
        items=artists,
        count=len(artists),
    )


@router.get("", response_model=ArtistCollection)
async def get_top_artists(query: ArtistQuery = Depends()) -> ArtistCollection:
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
    client = Client(query)
    return get_artists(client)


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
    client = Client(ArtistQuery())
    return get_artist(artist_id, client)
