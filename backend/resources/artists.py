"""Datafy Artists Resource"""

from typing import Tuple

from flask_restful import Resource

from resources.base import BaseService


class Artists(Resource, BaseService):
    """
    The artists resource defines the RESTful interactions available for Spotify
    artists

    Inherits:
    - BaseService: The service adapter interface
    """

    __name__ = "artists"

    def get(self) -> Tuple[list[str], int, dict]:
        """
        Retrieves the current user's top artists.

        Returns:
        - A tuple containing the list of top artists, the response status code,
        and a request headers object

        TODO: Implement query params
        """
        top_artists = self.client.current_user_top_artists(limit=5)
        return (
            [item["name"] for item in top_artists["items"]],
            200,
            {"Access-Control-Allow-Origin": "*"},
        )
