"""Defines the Songs Adapter class"""

from typing import Any

from adapters.base import Adapter


class SongsAdapter(Adapter):
    """Defines an adapter pattern for the Songs model"""

    def make_table(self) -> list[list[Any]]:
        """
        Converts the songs data into a list of rows

        Returns
        -------
        table: list[list[Any]]
            a list of rows which are lists of song ranks, names, artists, popularity,
            album, release date, and IDs
        """
        return [
            [
                idx + 1,
                item["name"],
                ", ".join(item["artists"]),
                item["popularity"],
                item["album"],
                item["release_date"],
                item["id"],
            ]
            for idx, item in enumerate(self.data["items"])
        ]
