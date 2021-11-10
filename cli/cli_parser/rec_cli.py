"""Defines the CLI for recommendation requests"""
import logging
from argparse import ArgumentParser, Namespace

from cli_parser.datafy_cli import DatafyCLI
from libs.url_builder import URLBuilder

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger("cli_logger")

TABLE_FIELDS = {"recs": ["Song", "Artists"]}


class RecCLI(DatafyCLI):
    """CLI application for making recommendation requests"""

    def __init__(self, base_uri: str = "http://0.0.0.0:5000") -> None:
        super().__init__(TABLE_FIELDS, base_uri)

    def parse_data(self, data: dict) -> list[list]:
        """Parses data according to the type of content being retrieved

        Params
        ------
        data: dict
            a dictionary of data retrieved from Spotify

        Returns
        -------
        parsed_data: list[list]
            a list of data rows
        """

        return [
            [
                song["song"],
                ", ".join(song["artists"]),
            ]
            for song in data["items"]
        ]

    def display_data(self, data: list[list]) -> None:
        """Displays the data retrieved from Spotify in the terminal as a formatted table

        Args
        ----
        - data [list[list]]: A list of data rows

        """
        self.table.field_names = self.table_fields["recs"]
        self.table.add_rows(data)
        print(self.table)

    def make_endpoint(self) -> None:
        """Constructs the API endpoint URL"""

        self.endpoint = (
            URLBuilder(self.base_uri)
            .with_resource("recommendations")
            .with_param(key="seed_artists", value=self.args.seed_artists)
            .with_param(key="seed_tracks", value=self.args.seed_tracks)
            .with_param(key="seed_genres", value=self.args.seed_genres)
            .with_param(key="limit", value=self.args.limit)
            .build()
        )
