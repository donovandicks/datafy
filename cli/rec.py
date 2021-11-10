"""The Datafy Recommendations CLI"""
from cli_parser.rec_cli import RecCLI

if __name__ == "__main__":

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
