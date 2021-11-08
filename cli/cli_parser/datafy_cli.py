"""Defines the DatafyCLI"""

import logging
from argparse import ArgumentParser, Namespace
from pprint import pprint
from typing import Any

from libs.url_builder import URLBuilder
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
        self.endpoint: str = ""

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

    def __parse_args(self):
        """Parses the args passed by the user"""
        self.args = self.parser.parse_args()
        return self

    def __display_args(self):
        """FOR DEBUGGING: Prints the parsed argument namespace to the terminal"""
        pprint(self.args)

    def __parse_data(self, data: dict) -> list[list]:
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

    def __send_request(self):
        """Sends a GET request to the API endpoint

        Returns
        -------
        response: dict
            the JSON response received from the API

        Raises
        ------
        RequestException
            if the response has a status code other than 200
        """
        response = get(self.endpoint)

        match response.status_code:
            case 200:
                return response.json()

            case _:
                logger.exception("Failed to make request to Datafy: %s", response.text)
                raise RequestException

    def __make_endpoint(self):
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


    def run_command(self):
        """Execute the command determined by the arguments passed to the CLI"""
        self.__parse_args()
        self.__make_endpoint()

        data = self.__send_request()

        parsed_data = self.__parse_data(data)
        self.display_data(parsed_data)
