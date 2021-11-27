"""The Genre query model"""

from typing import Optional

from pydantic import BaseModel, validator

from models.common import TimeRange


class GenreQuery(BaseModel):
    """The query model for the Genres resource"""

    time_range: Optional[TimeRange]
    aggregate: Optional[bool]
    limit: Optional[int]

    @validator("limit")
    def limit_is_positive(cls, lmt):  # pylint: disable=no-self-argument
        """Ensures that the limit passed is a positive value greater than 0"""
        if not lmt:
            return lmt

        if lmt <= 0:
            raise ValueError("limit must be at least 1")
        return lmt

    class Config:
        """Defines the configuration for the query model"""

        use_enum_values = True


class GenreResponse(BaseModel):
    """The object model of the response body for the genres endpoint"""

    items: dict[str, int]
