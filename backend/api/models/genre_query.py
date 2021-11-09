"""The Genre query model"""

from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from models.common import TimeRange


class GenreQuery(BaseModel):
    """The query model for the Genres resource"""

    time_range: Optional[TimeRange]
    aggregate: Optional[bool]
    limit: Optional[int]

    # @validator("content")
    # def content_must_be_songs_or_artists(
    #     cls, cont
    # ):  # pylint: disable=no-self-use, no-self-argument
    #     """Checks that the content is either artists or songs"""

    #     if cont not in ["artists", "songs"]:
    #         raise ValueError("Content passed not supported")

    #     return cont

    class Config:
        """Defines the configuration for the query model"""

        use_enum_values = True
