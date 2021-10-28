"""Datafy Songs Resource"""

from typing import Tuple

from flask import request
from flask_restful import Resource

from resources.base import BaseService


class Songs(Resource, BaseService):
    """
    The tracks resource defines the RESTful interactions available for Spotify
    songs

    Inherits:
    - BaseService: The service adapter interface
    """

    __name__ = "songs"

    def get(self) -> Tuple[list[dict], int, dict]:
        """
        Retrieves the current user's top songs.

        Returns:
        - A tuple containing a dict of song and artists, the response status
        code, and a request headers object

        TODO: Implement query params with marshmallow
        """
        print(request.args)

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
