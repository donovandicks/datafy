"""Query models for Spotify artists"""

from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from models.common import TimeRange


class ArtistModel(BaseModel):

    limit: Optional[int]
    time_range: Optional[TimeRange]

    class Config:
        use_enum_values = True
