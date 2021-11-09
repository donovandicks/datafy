"""Query models for Spotify artists"""

from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from models.common import TimeRange


class ArtistQuery(BaseModel):
    """The query model for the Artists resource"""

    limit: Optional[int]
    time_range: Optional[TimeRange]

    class Config:
        """Defines the configuration for the query model"""

        use_enum_values = True
