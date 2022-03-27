"""Main flow"""
from datetime import datetime, timedelta
from time import sleep
from typing import Tuple

from spotipy import Spotify

from clients.postgres import PostgresClient
from clients.spotify import init_spotify_client
from tasks.db import (
    check_counted,
    count_new_track,
    insert_album,
    insert_artist,
    insert_track,
    update_track_count,
)
from tasks.spotify import get_current_track
from telemetry.logging import logger, bind_pipeline


def init_clients() -> Tuple[Spotify, PostgresClient]:
    """Initializes various application clients"""
    logger.info("Initializing External Clients")
    return init_spotify_client(), PostgresClient()


def main_flow():
    """Main flow"""
    bind_pipeline()
    logger.bind()
    logger.info("BEGINNING PIPELINE EXECUTION")
    sp_client, db_client = init_clients()

    track = get_current_track(client=sp_client)

    if not track:
        return

    exists = check_counted(client=db_client, track=track)

    if exists:
        update_track_count(client=db_client, track=track, row=exists[0])
        return

    inserted_album = insert_album(client=db_client, track=track)
    inserted_artist = insert_artist(client=db_client, track=track)

    if not inserted_album or not inserted_artist:
        logger.error("ENDING PIPELINE EXECUTION WITH FAILURE")
        raise Exception(
            f"Failed to insert an album ({inserted_album}) or artist ({inserted_artist})"
        )

    inserted_track = insert_track(client=db_client, track=track)

    if not inserted_track:
        logger.error("ENDING PIPELINE EXECUTION WITH FAILURE")
        raise Exception("Failed to insert track")

    count_new_track(client=db_client, track=track)


def main():
    """Runs the flow"""
    while True:
        main_flow()
        sleep(30)


if __name__ == "__main__":
    main()
