"""Query models for Spotify recommendations"""

from typing import Any, Optional

from pydantic import BaseModel


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

    seed_artists: Optional[str]
    """A comma separated list of artist IDs"""

    seed_genres: Optional[str]
    """A comma separated list of genres"""

    seed_tracks: Optional[str]
    """A comma separated list of song IDs"""

    seed_artists_list: Optional[list[str]]
    """A Python list of seed artists - derived from `seed_artists`"""

    seed_genres_list: Optional[list[str]]
    """A Python list of seed genres - derived from `seed_genres`"""

    seed_tracks_list: Optional[list[str]]
    """A Python list of seed tracks - derived from `seed_tracks`"""

    limit: Optional[int]
    """The number of recommendations to retrieve"""

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.seed_artists_list = (
            self.seed_artists.split(",") if self.seed_artists else []
        )
        self.seed_genres_list = self.seed_genres.split(",") if self.seed_genres else []
        self.seed_tracks_list = self.seed_tracks.split(",") if self.seed_tracks else []
