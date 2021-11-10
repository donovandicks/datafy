"""Query models for Spotify recommendations"""

from typing import Optional

from pydantic import BaseModel, validator


class RecommendationQuery(BaseModel):
    """
    The query model for the Recommendations resource

    Examples
    --------
    - Recommendations for seed artists of Trav and Ye with a limit of 5
    curl http://localhost:5000/recommendations?seed_artists=5K4W6rqBFWDnAN6FQUkS6x,0Y5tJX1MQlPlqiwlOH1tJY&limit=5
    - just trav
    curl http://localhost:5000/recommendations?seed_artists=0Y5tJX1MQlPlqiwlOH1tJY&limit=5
    - just ye
    curl http://localhost:5000/recommendations?seed_artists=5K4W6rqBFWDnAN6FQUkS6x&limit=5

    - seed track of Orange Soda (he's baby keem)
    curl http://localhost:5000/recommendations?seed_tracks=5FkoSXiJPKTNyYgALRJFhD&limit=5

    - seed tracks of Fade and Waves
    curl http://localhost:5000/recommendations?seed_tracks=3cCxoOgfi6hgt8MNteuiiD,3nAq2hCr1oWsIU54tS98pL&limit=5
    """

    # just the required fields for now, want to add in things like target sounds and whatnot
    # although these are lists, they come in as a string and then are used to create the lists

    seed_artists: Optional[str | list[str]]
    """A comma separated list of artist IDs"""

    seed_genres: Optional[str | list[str]]
    """A comma separated list of genres"""

    seed_tracks: Optional[str | list[str]]
    """A comma separated list of song IDs"""

    limit: Optional[int]
    """The number of recommendations to retrieve"""

    @validator("seed_artists", "seed_genres", "seed_tracks")
    def _deserialize_seed_artists(cls, seeds: str | list): # pylint: disable=no-self-argument
        if not seeds:
            return None

        if isinstance(seeds, list):
            return seeds

        return seeds.split(",")
