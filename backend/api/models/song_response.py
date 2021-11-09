"""Defines the structure of the data returned by the songs response"""

from pydantic import BaseModel


class SongResponse(BaseModel):
    """The object model of the response body for the songs endpoint"""

    items: list[dict[str, str | list[str]]]
