"""Internal Track Model"""

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

    def __str__(self) -> str:
        return str(self.dict())

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
        )
