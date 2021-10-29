"""Datafy Songs Resource"""

from enum import Enum
from typing import Optional, Tuple

from flask_restful import Resource
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic_webargs import webargs

from resources.base import BaseService


class TimeRange(Enum):
    """The supported time ranges for the Spotify web API"""

    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"


class QueryModel(BaseModel):
    """
    The type definition for available query params on the Songs resource.
    Validates that request query params follow the below schema and makes working
    with their values easier
    """

    limit: Optional[int]
    time_range: Optional[TimeRange]

    class Config:
        """Configuration for the QueryModel"""

        use_enum_values = True  # Allows passing enum values in query params


class Songs(Resource, BaseService):
    """
    The tracks resource defines the RESTful interactions available for Spotify
    songs

    Inherits:
    - BaseService: The service adapter interface
    """

    __name__ = "songs"

    @webargs(query=QueryModel)
    def get(self, **kwargs) -> Tuple[list[dict], int, dict]:
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
