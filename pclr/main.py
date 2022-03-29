"""Main flow"""
from time import sleep
from typing import Tuple

from spotipy import Spotify

from clients.postgres import PostgresClient
from clients.spotify import init_spotify_client
from models.ops import Status, PipelineStatus
from models.db import is_playcount_list
from tasks.db import check_counted, update_track_count, insert_flow
from tasks.spotify import spotify_flow
from telemetry.logging import logger, bind_pipeline


def init_clients() -> Tuple[Spotify, PostgresClient]:
    """Initializes various application clients"""
    logger.info("Initializing External Clients")
    return init_spotify_client(), PostgresClient()


def main_flow() -> PipelineStatus:
    """Main flow"""
    bind_pipeline()
    logger.bind()
    logger.info("BEGINNING PIPELINE EXECUTION")

    pls = PipelineStatus(status=Status.NONE, operations=[])

    sp_client, db_client = init_clients()

    sp_flow = spotify_flow(client=sp_client, pls=pls)
    if isinstance(sp_flow, PipelineStatus):
        return sp_flow

    track = sp_flow
    exists = check_counted(client=db_client, track=track)
    pls.operations.append(exists)

    if exists.error:
        return pls.with_status(status=exists.status)

    if exists.data and is_playcount_list(val=exists.data):
        updated = update_track_count(client=db_client, track=track, row=exists.data[0])
        pls.operations.append(updated)
        return pls.with_status(updated.status)

    inserted = insert_flow(client=db_client, track=track, pls=pls)
    if not inserted:
        return pls.with_status(status=Status.FAILED)

    return pls.with_status(status=Status.COMPLETED)


def main():
    """Runs the flow"""
    while True:
        pls = main_flow()
        pls.log_status(logger=logger)
        sleep(30)


if __name__ == "__main__":
    main()
