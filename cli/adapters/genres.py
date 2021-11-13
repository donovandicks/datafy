"""Defines the Genres Adapter class"""

from typing import Any

from adapters.base import Adapter


class GenresAdapter(Adapter):
    """Defines an adapter pattern for the Genres model"""

    def make_table(self) -> list[list[Any]]:
        """
        Converts the genres data into a list of rows

        Returns
        -------
        table: list[list[Any]]
            a list of rows which are lists of genres and counts
        """
        return [
            [
                genre,
                count,
            ]
            for genre, count in self.data["items"].items()
        ]
