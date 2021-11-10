"""The Datafy CLI"""
from cli_parser.datafy_cli import DatafyCLI
from cli_parser.api_cli import APICLI
from cli_parser.rec_cli import RecCLI

if __name__ == "__main__":
    # plan to work with different clis:
    # - running this main file will ask you which you want to use
    # - create the instance of that cli
    # - then take in the arguments for that cli
    """
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
    """

    RecCLI().add_argument(
        "-sa",
        "--seed_artists",
        arg_type=str,
        arg_help="The seed artists to generate the recommendations from",
        req=False,
        default=None,
    ).add_argument(
        "-st",
        "--seed_tracks",
        arg_type=str,
        arg_help="The seed tracks to generate the recommendations from",
        req=False,
        default=None,
    ).add_argument(
        "-sg",
        "--seed_genres",
        arg_type=str,
        arg_help="The seed genres to generate the recommendations from",
        req=False,
        default=None,
    ).add_argument(
        "-l",
        "--limit",
        arg_type=int,
        arg_help="The maximum number of results to retrieve",
        req=False,
        default=20,
    ).run_command()
