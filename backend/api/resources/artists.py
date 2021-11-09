"""Defines the API logic for the /artists endpoint"""

from typing import Any

from flask import current_app as app
from flask.wrappers import Response
from flask_restful import NotFound, Resource
from models.artist_query import ArtistQuery
from models.artist_response import ArtistResponse
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

    def __get_response_body(self, query: ArtistQuery) -> ArtistResponse:
        top_artists = self.client.current_user_top_artists(
            limit=query.limit,
            time_range=query.time_range,
        )

        if not top_artists:
            app.logger.error("Failed to retrieve top artists")
            raise NotFound

        return ArtistResponse(items=[item["name"] for item in top_artists["items"]])

    @webargs(query=ArtistQuery)
    def get(self, **kwargs) -> Response:
        """
        Retrieves the current user's top artists.

        Returns:
        - A tuple containing the list of top artists, the response status code,
        and a request headers object
        """
        response_body = self.__get_response_body(ArtistQuery(**kwargs["query"]))

        return Response(
            response=response_body.json(),
            status=200,
            headers={"Access-Control-Allow-Origin": "*"},
        )
