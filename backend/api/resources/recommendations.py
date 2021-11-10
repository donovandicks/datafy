"""Defines the API logic for the /recommendations endpoint"""

from flask import current_app as app
from flask.wrappers import Response
from flask_restful import NotFound, Resource
from models.recommendation_query import RecommendationQuery
from models.recommendation_response import RecommendationResponse
from pydantic_webargs import webargs

from resources.base import BaseService


class Recommendations(Resource, BaseService):
    """
    The recommendations resource defines the RESTful interactions available for
    Spotify recommendations

    Inherits:
    - BaseService: The service adapter interface
    """

    def __init__(self) -> None:
        self.query = RecommendationQuery()
        super().__init__()

    def __format_seed_lists(self) -> None:
        """Turns Strings of comma separated values into lists of Strings"""

        self.query.seed_artists = (
            self.query.seed_artists.split(",")
            if self.query.seed_artists
            else None
        )
        self.query.seed_genres = (
            self.query.seed_genres.split(",")
            if self.query.seed_genres
            else None
        )
        self.query.seed_tracks = (
            self.query.seed_tracks.split(",")
            if self.query.seed_tracks
            else None
        )

    def __get_response_body(self) -> RecommendationResponse:
        self.__format_seed_lists()

        recommendations = self.client.recommendations(
            seed_artists=self.query.seed_artists,
            seed_genres=self.query.seed_genres,
            seed_tracks=self.query.seed_tracks,
            limit=self.query.limit,
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
