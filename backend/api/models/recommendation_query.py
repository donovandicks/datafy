"""Query models for Spotify recommendations"""

from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class RecommendationQuery(BaseModel):
    """The query model for the Recommendations resource"""

    # just the required fields for now, want to add in things like target sounds and whatnot
    # all must be a str comma separated list of some sort of spotify id
    seed_artists: Optional[str]
    seed_genres: Optional[str]
    seed_tracks: Optional[str]

    class Config:
        """Defines the configuration for the query model"""

        # i don't think this line is necessary for the rec model
        # use_enum_values = True
