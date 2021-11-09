"""Query models for Spotify songs"""

from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from models.common import TimeRange


class SongQuery(BaseModel):
    """
    The type definition for available query params on the Songs resource.

    Members:
    - limit {Optional[int]}: The maximum number of songs to return in a single request
    - time_range {Optional[TimeRange]}: The time period from which to retrieve the requested data

    Inherits:
    - BaseModel: The pydantic base data model
    """

    limit: Optional[int]
    time_range: Optional[TimeRange]

    class Config:
        """Configuration for the QueryModel"""

        use_enum_values = True  # Allows passing enum values in query params
