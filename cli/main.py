"""The Datafy CLI"""

from argparse import ArgumentParser, Namespace
from pprint import pprint
from typing import Any, Type

from prettytable import PrettyTable
from requests import get

TABLE_FIELDS = {
    "artists": ["Rank", "Artist"],
    "songs": ["Rank", "Song", "Artists"],
}


class DatafyCLI:
    """The CLI Application for interacting with Spotify data from the terminal"""

    def __init__(self) -> None:
        """Initializes the CLI application with the ArgumentParser instance"""

        self.parser = ArgumentParser(description="""
A CLI application designed to interact with the Datafy backend from a terminal.
        """)

        self.args: Namespace = Namespace()
        self.table: PrettyTable = PrettyTable()

    def add_argument(self, *name, arg_type: Type, choices: list[Any], arg_help: str):
        """Add an argument to the CLI's argument parser

        Args
        ----
        - *name [str|list[str]]: The name or tack-name of the argument, e.g. path or -p or --path
        - arg_type [Type]: The primitive that the argument value should match and be coerced into
        - choices [list[Any]]: The possible choices a user can make for the argument value
        - arg_help [str]: The help message displayed in the terminal for this argument
        """
        self.parser.add_argument(
            *name, type=arg_type, choices=choices, help=arg_help, required=True
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

        Args
        ----
        - data [dict]: A dictionary of data retrieved from Spotify

        Returns
        -------
        - [list[list]]: A list of data rows
        """
        if self.args.content == "songs":
            return [
                [
                    idx + 1, song["song"], ", ".join(song["artists"]),
                ] for idx, song in enumerate(data)
            ]

        if self.args.content == "artists":
            return [
                [
                    idx + 1, artist,
                ] for idx, artist in enumerate(data)
            ]

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

    def run_command(self):
        """Execute the command determined by the arguments passed to the CLI"""
        self._parse_args()

        response = get(f"http://0.0.0.0:5000/{self.args.content}?time_range={self.args.time_range}")

        match response.status_code:
            case 200:
                parsed_data = self._parse_data(response.json())
                self.display_data(parsed_data)

            case _:
                print(f"Failed to make request to Datafy: {response.text}")


if __name__ == "__main__":
    DatafyCLI().add_argument(
        "-c",
        "--content",
        arg_type=str,
        choices=["songs", "artists"],
        arg_help="The type of content to retrieve, songs or artists",
    ).add_argument(
        "-t",
        "--time_range",
        arg_type=str,
        choices=["short_term", "medium_term", "long_term"],
        arg_help="The time period from which to retrieve data",
    ).run_command()
