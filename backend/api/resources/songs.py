"""Datafy Songs Resource"""

from flask import current_app as app
from flask.wrappers import Response
from flask_restful import NotFound, Resource
from models.song_query import SongQuery
from models.song_response import SongResponse
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

    def __init__(self) -> None:
        self.query = SongQuery()
        super().__init__()

    def __get_response_body(self) -> SongResponse:
        """Retrieves the body data for the response object

        Returns
        -------
        SongResponse
            the data model containing a list of songs and their artists
        """
        top_tracks = self.client.current_user_top_tracks(
            limit=self.query.limit,
            time_range=self.query.time_range,
        )

        if not top_tracks:
            app.logger.error("Failed to retrieve top artists")
            raise NotFound

        return SongResponse(
            items=[
                {
                    "song": item["name"],
                    "artists": [artist["name"] for artist in item["artists"]],
                }
                for item in top_tracks["items"]
            ],
        )

    @webargs(query=SongQuery)
    def get(self, **kwargs) -> Response:
        """
        Retrieves the current user's top songs.

        Returns:
        - A tuple containing a dict of song and artists, the response status
        code, and a request headers object
        """
        self.query = SongQuery(**kwargs["query"])
        app.logger.info("Retrieving song data with parameters: %r", self.query)

        return Response(
            response=self.__get_response_body().json(),
            status=200,
            headers={"Access-Control-Allow-Origin": "*"},
        )
