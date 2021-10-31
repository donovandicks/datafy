"""Datafy Artists Resource"""

from typing import Tuple

from flask_restful import Resource
from models.artist_query import ArtistModel
from pydantic_webargs import webargs

from resources.base import BaseService


class Artists(Resource, BaseService):
    """
    The artists resource defines the RESTful interactions available for Spotify
    artists

    Inherits:
    - BaseService: The service adapter interface
    """

    __name__ = "artists"


    @webargs(query=ArtistModel)
    def get(self, **kwargs) -> Tuple[list[str], int, dict]:
        """
        Retrieves the current user's top artists.

        Returns:
        - A tuple containing the list of top artists, the response status code,
        and a request headers object
        """
        params = kwargs["query"]
        top_artists = self.client.current_user_top_artists(
            limit=params["limit"],
            time_range=params["time_range"],
        )

        return (
            [item["name"] for item in top_artists["items"]],
            200,
            {"Access-Control-Allow-Origin": "*"},
        )
