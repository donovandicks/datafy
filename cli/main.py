"""The Datafy CLI"""

import logging
from argparse import ArgumentParser, Namespace
from pprint import pprint
from typing import Any

from prettytable import PrettyTable
from requests import RequestException, get

TABLE_FIELDS = {
    "artists": ["Rank", "Artist"],
    "songs": ["Rank", "Song", "Artists"],
    "genres": ["Genre", "Count"],
}

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger("cli_logger")

class DatafyCLI:
    """The CLI Application for interacting with Spotify data from the terminal"""

    def __init__(self, base_uri: str = "http://0.0.0.0:5000") -> None:
        """Initializes the CLI application with the ArgumentParser instance"""

        self.parser = ArgumentParser(description="""
A CLI application designed to interact with the Datafy backend from a terminal.
        """)

        self.args: Namespace = Namespace()
        self.table: PrettyTable = PrettyTable()
        self.base_uri: str = base_uri

    def add_argument(
        self,
        *name: str,
        arg_type: type,
        choices: list[Any] = None,
        arg_help: str,
        req: bool = True,
        default: Any = None,
    ):
        """Add an argument to the CLI's argument parser

        Params
        ------
        *name: str|list[str]
            the name or tack-name of the argument, e.g. path or -p or --path
        arg_type: Type
            the primitive that the argument value should match and be coerced into
        choices: list[Any]
            the possible choices a user can make for the argument value
        arg_help: str
            the help message displayed in the terminal for this argument
        """
        self.parser.add_argument(
            *name, type=arg_type, choices=choices, help=arg_help, required=req, default=default,
        )
        return self

    def _parse_args(self):
        """Parses the args passed by the user"""
        self.args = self.parser.parse_args()
        return self

    def _display_args(self):
        """FOR DEBUGGING: Prints the parsed argument namespace to the terminal"""
        pprint(self.args)

    def _parse_data(self, data: dict) -> list[list]:
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

    def display_data(self, data: list[list]):
        """Displays the data retrieved from Spotify in the terminal as a formatted table

        Args
        ----
        - data [list[list]]: A list of data rows

        """
        self.table.field_names = TABLE_FIELDS[self.args.content]
        self.table.add_rows(data)
        print(self.table)

    def _send_request(self, endpoint):
        response = get(endpoint)

        match response.status_code:
            case 200:
                return response.json()

            case _:
                logger.exception("Failed to make request to Datafy: %s", response.text)
                raise RequestException

    def run_command(self):
        """Execute the command determined by the arguments passed to the CLI"""
        self._parse_args()

        endpoint = ""
        match self.args:
            case Namespace(content="genres", time_range=str(rng), aggregate=bool(agg),
                            limit=int(lmt)):
                endpoint = f"{self.base_uri}/genres?time_range={rng}&aggregate={agg}&limit={lmt}"

            case Namespace(content=str(content), time_range=str(rng), limit=int(lmt)):
                endpoint = f"{self.base_uri}/{content}?time_range={rng}&limit={lmt}"

            case _:
                logger.exception("Unsupported CLI arguments passed %r", self.args)

        data = self._send_request(endpoint)

        parsed_data = self._parse_data(data)
        self.display_data(parsed_data)


if __name__ == "__main__":
    DatafyCLI().add_argument(
        "-c",
        "--content",
        arg_type=str,
        choices=["songs", "artists", "genres"],
        arg_help="The type of content to retrieve, songs or artists",
    ).add_argument(
        "-t",
        "--time_range",
        arg_type=str,
        choices=["short_term", "medium_term", "long_term"],
        arg_help="The time period from which to retrieve data",
        req=False,
        default="medium_term",
    ).add_argument(
        "-a",
        "--aggregate",
        arg_type=bool,
        arg_help="Set to True to get an aggregated genre count",
        req=False,
        default=False,
    ).add_argument(
        "-l",
        "--limit",
        arg_type=int,
        arg_help="The maximum number of results to retrieve",
        req=False,
        default=50,
    ).run_command()
