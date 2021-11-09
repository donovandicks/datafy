"""Defines the structure of the data returned by the /artists response"""

from pydantic import BaseModel


class ArtistResponse(BaseModel):
    """The object model of the response body for the /artists endpoint"""

    items: list[str]
