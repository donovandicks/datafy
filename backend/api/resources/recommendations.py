"""Defines the API logic for the /recommendations endpoint"""

from flask import current_app as app
from flask.wrappers import Response
from flask_restful import NotFound, Resource
from models.artist_query import RecommendationQuery
from models.artist_response import RecommendationResponse
from pydantic_webargs import webargs

from resources.base import BaseService


class Recommendations(Resouce, BaseService):
    """
    The recommendations resource defines the RESTful interactions available for
    Spotify recommendations

    Inherits:
    - BaseService: The service adapter interface
    """

    def __init__(self) -> None:
        self.query = RecommendationQuery()
        super().__init__()

    """
    FUNCTIONS I KNOW I WANT/NEED:
    - get
    - __get_response_body
    """

    def __get_response_body(self) -> RecommendationResponse:
        recommendations = self.client.recommendations(
            seed_artists=self.query.seed_artists,
            seed_genres=self.query.seed_genres,
            seed_tracks=self.query.seed_tracks,
        )

        if not recommendations:
            app.logger.error("Failed to retrieve recommendations")
            raise NotFound

        # this is just the same as a regular songs query for now
        return RecommendationResponse(
            items=[
                {
                    "song": item["name"],
                    "artists": [artist["name"] for artist in item["artists"]],
                }
                for item in recommendations["tracks"]
            ],
        )

    @webargs(query=RecommendationQuery)
    def get(self, **kwargs) -> Response:
        """Retrieves the recommendations"""
        self.query = RecommendationQuery(**kwargs["query"])
        app.logger.info(
            "Retrieving recommendation data with parameters: %r", self.query
        )

        return Response(
            response=self.__get_response_body().json(),
            status=200,
            headers={"Access-Control-Allow-Origin": "*"},
        )
