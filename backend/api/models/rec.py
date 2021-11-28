"""Query models for Spotify recommendations"""

from typing import Any, Dict, Optional

from pydantic import BaseModel

from .common import Query


class RecQuery(Query):
    """
    The query model for the `/recs` route

    Examples
    --------
    - Recommendations for seed artists of Trav and Ye with a limit of 5
    curl {base}/recs?seed_artists=5K4W6rqBFWDnAN6FQUkS6x,0Y5tJX1MQlPlqiwlOH1tJY&limit=5
    - just trav
    curl {base}/recs?seed_artists=0Y5tJX1MQlPlqiwlOH1tJY&limit=5
    - just ye
    curl {base}/recs?seed_artists=5K4W6rqBFWDnAN6FQUkS6x&limit=5

    - seed track of Orange Soda (he's baby keem)
    curl {base}/recs?seed_tracks=5FkoSXiJPKTNyYgALRJFhD&limit=5

    - seed tracks of Fade and Waves
    curl {base}/recs?seed_tracks=3cCxoOgfi6hgt8MNteuiiD,3nAq2hCr1oWsIU54tS98pL&limit=5
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

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.seed_artists_list = self.seed_artists.split(",") if self.seed_artists else []
        self.seed_genres_list = self.seed_genres.split(",") if self.seed_genres else []
        self.seed_tracks_list = self.seed_tracks.split(",") if self.seed_tracks else []


class Rec(BaseModel):
    """The model for a recommendation item"""

    song: str
    artists: list[str]

    @classmethod
    def from_dict(cls, rec: Dict):
        """Converts a dict into a `Rec` object"""
        return Rec(
            song=rec["name"],
            artists=[artist["name"] for artist in rec["artists"]],
        )


class RecCollection(BaseModel):
    """The response body for the `/recs` route"""

    items: list[Rec]
    """A list of recommended songs"""

    count: int
    """The number of items in the collection"""
