"""Internal Track Model"""

from pydantic import BaseModel, ValidationError


class Track(BaseModel):
    """
    An internal model for Spotify tracks. The model contains a reduced information
    set to save space and strip out unused information from the Spotify API.
    """

    id: str
    """The Spotify Track ID"""

    name: str
    """The name of the Track"""

    @classmethod
    def from_dict(cls, obj: dict):
        """
        Converts an object to a `Track` object
        """
        if "item" not in obj:
            raise ValidationError("`item` not found in object", Track)

        item = obj.get("item", {})

        return Track(id=item.get("id", ""), name=item.get("name", ""))
