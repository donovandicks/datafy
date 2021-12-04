"""Defines the logic for handling requests to the `/artists` route"""
from dependencies.spotify import Client, SpotifyClient
from fastapi import APIRouter, Depends
from models.artist import Artist, ArtistQuery
from models.collection import Collection

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


def get_artists(client: SpotifyClient) -> Collection[Artist]:
    """
    Retrieves a list of artists from Spotify formatted as an `ArtistResponse`

    Params
    ------
    client: SpotifyClient
        a api client object used to connect to Spotify

    Returns
    -------
    artists: Collection[Artist]
        a collection of `Artist` objects
    """
    artists = [Artist.from_dict(item) for item in client.get_artists_from_spotify()]
    return Collection.from_list(artists)


@router.get("", response_model=Collection[Artist])
async def get_top_artists(query: ArtistQuery = Depends()) -> Collection[Artist]:
    """
    Retrieves the current users top artists from the spotify api

    Params
    ------
    query: ArtistQuery
        the query params included in the endpoint URL

    Returns
    -------
    artists: Collection[Artist]
        a collection of `Artist` objects
    """
    return get_artists(Client(query))


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
    return get_artist(artist_id, Client(ArtistQuery()))
