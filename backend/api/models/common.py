"""Common model definitions across API query models"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator


class TimeRange(Enum):
    """The supported time ranges for the Spotify web API

    short_term = The last 4 weeks
    medium_term = The last 6 months
    long_term = The last several years
    """

    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"


class Query(BaseModel):
    """Common query model"""

    limit: Optional[int]
    time_range: Optional[TimeRange]

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
