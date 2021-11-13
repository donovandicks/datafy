"""Defines the structure of the data returned by the recommendations response"""

from pydantic import BaseModel


class Recommendation(BaseModel):
    """The object model for a recommendation item"""

    song: str
    artists: list[str]


class RecommendationResponse(BaseModel):
    """The object model of the response body for the artists endpoint"""

    # assuming this just sends back a list of tracks, this is copied from the song response file
    items: list[Recommendation]
