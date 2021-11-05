"""Datafy Songs Resource"""

from typing import Tuple

from flask_restful import NotFound, Resource
from models.song_query import SongModel
from pydantic_webargs import webargs

from resources.base import BaseService


class Songs(Resource, BaseService):
    """
    The tracks resource defines the RESTful interactions available for Spotify
    songs

    Inherits:
    - BaseService: The service adapter interface
    """

    __name__ = "songs"

    @webargs(query=SongModel)
    def get(self, **kwargs) -> Tuple[dict[str, list[dict]], int, dict]:
        """
        Retrieves the current user's top songs.

        Returns:
        - A tuple containing a dict of song and artists, the response status
        code, and a request headers object
        """
        params = kwargs["query"]

        top_tracks = self.client.current_user_top_tracks(
            limit=params["limit"],
            time_range=params["time_range"],
        )

        if not top_tracks:
            print("Failed to retrieve top artists")
            raise NotFound

        return (
            {
                "items": [
                    {
                        "song": item["name"],
                        "artists": [artist["name"] for artist in item["artists"]],
                    }
                    for item in top_tracks["items"]
                ]
            },
            200,
            {"Access-Control-Allow-Origin": "*"},
        )
