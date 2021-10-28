"""Datafy Artists Service"""
from pprint import pprint

from flask import Flask
from flask_restful import Api, Resource, reqparse
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from config import settings

SCOPES = "  ".join(
    [
        "ugc-image-upload",
        "playlist-modify-private",
        "playlist-read-private",
        "playlist-modify-public",
        "playlist-read-collaborative",
        "user-read-private",
        "user-read-playback-state",
        "user-modify-playback-state",
        "user-read-currently-playing",
        "user-library-modify",
        "user-library-read",
        "user-read-playback-position",
        "user-read-recently-played",
        "user-top-read",
        "app-remote-control",
        "streaming",
        "user-follow-modify",
        "user-follow-read",
    ]
)


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("task")


class TopArtists(Resource):
    def __init__(self) -> None:
        self.client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=settings["CLIENT_ID"],
                client_secret=settings["CLIENT_SECRET"],
                redirect_uri=settings["REDIRECT_URI"],
                scope=SCOPES,
            )
        )
        super().__init__()

    def get(self):
        top_artists = self.client.current_user_top_artists(limit=5)
        return (
            [item["name"] for item in top_artists["items"]],
            200,
            {"Access-Control-Allow-Origin": "*"},
        )


class TopTracks(Resource):
    def __init__(self) -> None:
        self.client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=settings["CLIENT_ID"],
                client_secret=settings["CLIENT_SECRET"],
                redirect_uri=settings["REDIRECT_URI"],
                scope=SCOPES,
            )
        )
        super().__init__()

    def get(self):
        top_tracks = self.client.current_user_top_tracks(limit=5)
        return (
            [
                {
                    "song": item["name"],
                    "artists": [artist["name"] for artist in item["artists"]],
                }
                for item in top_tracks["items"]
            ],
            200,
            {"Access-Control-Allow-Origin": "*"},
        )


api.add_resource(TopArtists, "/topartists")
api.add_resource(TopTracks, "/toptracks")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
