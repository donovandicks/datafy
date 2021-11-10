"""Defines the API logic for the /artists endpoint"""

from flask import current_app as app
from flask.wrappers import Response
from flask_restful import NotFound, Resource
from models.artist_query import ArtistQuery
from models.artist_response import Artist, ArtistResponse
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

    def __init__(self) -> None:
        self.query = ArtistQuery()
        super().__init__()

    def __get_response_body(self) -> ArtistResponse:
        """Retrieves the body data for the response object

        Returns
        -------
        ArtistResponse
            the data model object containing a list of artist names
        """
        top_artists = self.client.current_user_top_artists(
            limit=self.query.limit,
            time_range=self.query.time_range,
        )

        if not top_artists:
            app.logger.error("Failed to retrieve top artists")
            raise NotFound

        return ArtistResponse(
            items=[
                Artist(
                    id=item["id"],
                    name=item["name"],
                    popularity=item["popularity"],
                    followers=item["followers"]["total"],
                )
                for item in top_artists["items"]
            ]
        )

    @webargs(query=ArtistQuery)
    def get(self, **kwargs) -> Response:
        """
        Retrieves the current user's top artists.

        Returns:
        - A tuple containing the list of top artists, the response status code,
        and a request headers object
        """
        self.query = ArtistQuery(**kwargs["query"])
        app.logger.info("Retrieving top artists with params: %r", self.query)

        return Response(
            response=self.__get_response_body().json(),
            status=200,
            headers={"Access-Control-Allow-Origin": "*"},
        )
