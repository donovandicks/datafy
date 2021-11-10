"""Defines the CLI for top artist, song, and genre requests"""

import logging
from argparse import ArgumentParser, Namespace

from cli_parser.datafy_cli import DatafyCLI
from libs.url_builder import URLBuilder

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger("cli_logger")

TABLE_FIELDS = {
    "artists": ["Rank", "Artist"],
    "songs": ["Rank", "Song", "Artists"],
    "genres": ["Genre", "Count"],
}

class APICLI(DatafyCLI):
    """CLI application for making artist, song, and genre requests"""

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
        match self.args.content:
            case "songs":
                return [
                    [
                        idx + 1, song["song"], ", ".join(song["artists"]),
                    ] for idx, song in enumerate(data["items"])
                ]

            case "artists":
                return [
                    [
                        idx + 1, artist,
                    ] for idx, artist in enumerate(data["items"])
                ]

            case "genres" if data:
                return [
                    [
                        genre, count,
                    ] for genre, count in data["items"].items()
                ]

            case _:
                logging.warning("Unsupported content type")
                return [[]]

    def display_data(self, data: list[list]) -> None:
        """Displays the data retrieved from Spotify in the terminal as a formatted table

        Args
        ----
        - data [list[list]]: A list of data rows

        """
        self.table.field_names = self.table_fields[self.args.content]
        self.table.add_rows(data)
        print(self.table)

    def make_endpoint(self) -> None:
        """Constructs the API endpoint URL"""
        match self.args:
            case Namespace(
                content="genres",
                time_range=str(rng),
                aggregate=bool(agg),
                limit=int(lmt)
            ):
                self.endpoint = URLBuilder(self.base_uri) \
                    .with_resource("genres") \
                    .with_param(key="time_range", value=rng) \
                    .with_param(key="aggregate", value=agg) \
                    .with_param(key="limit", value=lmt) \
                    .build()

            case Namespace(content=str(content), time_range=str(rng), limit=int(lmt)):
                self.endpoint = URLBuilder(self.base_uri) \
                    .with_resource(content) \
                    .with_param(key="time_range", value=rng) \
                    .with_param(key="limit", value=lmt) \
                    .build()

            case _:
                logger.exception("Unsupported CLI arguments passed %r", self.args)
