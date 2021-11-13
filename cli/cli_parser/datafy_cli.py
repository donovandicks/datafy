"""Defines the abstract class for the DatafyCLI"""

import logging
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from pprint import pprint
from typing import Any

from prettytable import PrettyTable
from requests import RequestException, get
from yaml import YAMLError, safe_load

logging.basicConfig(level=logging.NOTSET)


def load_table_fields(file_path: str) -> dict[str, str]:
    """
    Loads the CLI table yaml config

    Parameters
    ----------
    file_path: str
        the module-relative path to the YAML config file, e.g. `templates/cli_tables.yaml`

    Returns
    -------
    table_fields: dict[str, str]
        the dictionary mapping created from the yaml file
    """
    with open(file_path, encoding="utf-8") as yaml_file:
        try:
            yml = safe_load(yaml_file)
            return yml.get("table_fields", {})

        except YAMLError as ex:
            raise Exception(f"Failed to load YAML file: {ex}") from YAMLError


class DatafyCLI(ABC):
    """The CLI Application for interacting with Spotify data from the terminal"""

    def __init__(
        self,
        table_fields_file_path: str,
        base_uri: str,
    ) -> None:
        """Initializes the CLI application with the ArgumentParser instance"""

        self.logger = logging.getLogger(__name__)
        self.parser = ArgumentParser(
            description="""
A CLI application designed to interact with the Datafy backend from a terminal.
        """
        )

        self.args: Namespace = Namespace()
        self.table: PrettyTable = PrettyTable()
        self.base_uri: str = base_uri
        self.endpoint: str = ""
        self.table_fields: dict = load_table_fields(table_fields_file_path)

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
            *name,
            type=arg_type,
            choices=choices,
            help=arg_help,
            required=req,
            default=default,
        )
        return self

    def __parse_args(self):
        """Parses the args passed by the user"""
        self.args = self.parser.parse_args()
        return self

    def __display_args(self):  # pylint: disable=unused-private-member
        """FOR DEBUGGING: Prints the parsed argument namespace to the terminal"""
        pprint(self.args)

    @abstractmethod
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

    def display_data(self, data: list[list]) -> None:
        """Displays the data retrieved from Spotify in the terminal as a formatted table

        Args
        ----
        - data [list[list]]: A list of data rows

        """
        self.table.field_names = self.table_fields[self.args.content]
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

        if response.status_code == 200:
            return response.json()

        self.logger.exception("Failed to make request to Datafy: %s", response.text)
        raise RequestException

    @abstractmethod
    def make_endpoint(self) -> None:
        """Constructs the API endpoint URL"""

    def run_command(self):
        """Execute the command determined by the arguments passed to the CLI"""
        self.__parse_args()
        self.make_endpoint()

        data = self.__send_request()

        parsed_data = self.parse_data(data)
        self.display_data(parsed_data)
