"""Defines the Artists Adapter class"""

from typing import Any

from adapters.base import Adapter


class ArtistsAdapter(Adapter):
    """Defines an adapter pattern for the Artists model"""

    def make_table(self) -> list[list[Any]]:
        """
        Converts the artists data into a list of rows

        Returns
        -------
        table: list[list[Any]]
            a list of rows which are lists of artist ranks, name, popularity,
            followers, and IDs
        """
        return [
            [
                idx + 1,
                item["name"],
                item["popularity"],
                item["followers"],
                item["id"],
            ]
            for idx, item in enumerate(self.data["items"])
        ]
