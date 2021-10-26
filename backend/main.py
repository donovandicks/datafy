"""Datafy Backend"""
from pprint import pprint

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from backend.config import settings

SCOPE = " ".join(
    [
        "user-library-read",
        "user-read-playback-position",
        "user-read-playback-state",
        "user-read-currently-playing",
        "user-read-recently-played",
        "user-top-read",
        "user-follow-read",
        "playlist-read-private",
        "playlist-read-collaborative",
    ]
)

sp = Spotify(
    auth_manager=SpotifyOAuth(
        client_id=settings["client_id"],
        client_secret=settings["client_secret"],
        scope=SCOPE,
        redirect_uri="http://localhost:8080",
    )
)

top_artists = sp.current_user_top_artists(limit=5)
top_artists_names = [item["name"] for item in top_artists["items"]]
pprint({"Top Artists": top_artists_names})

currently_playing = sp.currently_playing()["item"]
song_name = currently_playing["name"]
artists = " ".join([artist["name"] for artist in currently_playing["artists"]])

pprint({"Currently Playing": f"{song_name} by {artists}"})
