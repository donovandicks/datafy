"""Internal Track Model"""

import math
from typing import Dict

from pydantic import BaseModel, ValidationError  # pylint: disable=no-name-in-module


class Track(BaseModel):
    """
    An internal model for Spotify tracks. The model contains a reduced information
    set to save space and strip out unused information from the Spotify API.
    """

    timestamp: int

    track_id: str
    """The Spotify Track ID"""

    track_name: str
    """The name of the Track"""

    artist_id: str

    artist_name: str

    album_id: str

    album_name: str

    duration: int

    progress: int

    popularity: int

    def __str__(self) -> str:
        return str(self.dict())

    def get_id(self, item: str):
        """Retrieves the identifier for the given item"""
        match item:
            case "artist":
                return self.artist_id
            case "track":
                return self.track_id
            case "album":
                return self.album_id
            case _:
                raise ValueError(f"Item {item} does not have a valid identifier")

    @property
    def progress_pct(self) -> float:
        """Retrieve the current song progress as a percentage"""
        return (self.progress / self.duration) * 100

    @property
    def remaining(self) -> int:
        """Retrieves the number of milliseconds remaining in the track"""
        return self.duration - self.progress

    @property
    def remaining_seconds(self) -> int:
        """Retrieves the number of seconds remaining in the track"""
        return math.ceil(self.remaining / 1000)

    @classmethod
    def from_dict(cls, obj: Dict):
        """
        Converts an object to a `Track` object
        """
        if "item" not in obj:
            raise ValidationError("`item` not found in object", Track)

        item = obj.get("item", {})
        artists = item.get("artists", [])
        album = item.get("album", {})

        return Track(
            timestamp=obj.get("timestamp", 0),
            track_id=item.get("id", ""),
            track_name=item.get("name", ""),
            artist_id=artists[0].get("id", ""),
            artist_name=artists[0].get("name", ""),
            album_id=album.get("id", ""),
            album_name=album.get("name", ""),
            duration=item.get("duration_ms", 0),
            progress=obj.get("progress_ms", 0),
            popularity=item.get("popularity", 0),
        )
