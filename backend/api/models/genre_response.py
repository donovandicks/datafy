"""Defines the structure of the data returned by the genres response"""

from pydantic import BaseModel


class GenreResponse(BaseModel):
    """The object model of the response body for the genres endpoint"""

    items: dict[str, int]
