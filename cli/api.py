"""The Datafy API CLI"""
from cli_parser.api_cli import APICLI

if __name__ == "__main__":

    APICLI().add_argument(
        "-c",
        "--content",
        arg_type=str,
        choices=["songs", "artists", "genres"],
        arg_help="The type of content to retrieve: songs, artists, or genres",
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
