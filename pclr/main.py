"""Main flow"""
from time import sleep
from typing import List, Tuple, Union

from spotipy import Spotify

from clients.postgres import PostgresClient
from clients.spotify import init_spotify_client
from models.ops import Status, PipelineStatus
from models.db import PlayCount
from models.track import CurrentlyPlaying
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


def update_flow(
    client: PostgresClient,
    track: CurrentlyPlaying,
    pls: PipelineStatus,
    row: List[PlayCount],
) -> PipelineStatus:
    updated = update_track_count(client=client, track=track, row=row[0])
    pls.operations.append(updated)

    if updated.error:
        return pls

    pls.status = Status.COMPLETED
    return pls


def spotify_flow(client: Spotify, pls: PipelineStatus) -> Union[CurrentlyPlaying, None]:
    """"""
    track_task = get_current_track(client=client)
    pls.operations.append(track_task)

    if track_task.status in [Status.NO_CONTENT, Status.NOT_APPLICABLE]:
        pls.status = Status.COMPLETED
        return None

    if not track_task.data:
        return None

    return track_task.data


def insert_flow(
    client: PostgresClient, track: CurrentlyPlaying, pls: PipelineStatus
) -> bool:
    inserted_album = insert_album(client=client, track=track)
    pls.operations.append(inserted_album)
    inserted_artist = insert_artist(client=client, track=track)
    pls.operations.append(inserted_artist)

    if not inserted_album.data or not inserted_artist.data:
        return False

    inserted_track = insert_track(client=client, track=track)
    pls.operations.append(inserted_track)

    if not inserted_track.data:
        return False

    counted = count_new_track(client=client, track=track)
    pls.operations.append(counted)

    if counted.error:
        return False

    return True


def main_flow() -> PipelineStatus:
    """Main flow"""
    bind_pipeline()
    logger.bind()
    logger.info("BEGINNING PIPELINE EXECUTION")

    pls = PipelineStatus(status=Status.FAILED, operations=[])

    sp_client, db_client = init_clients()

    track = spotify_flow(client=sp_client, pls=pls)

    if not track:
        return pls

    exists = check_counted(client=db_client, track=track)
    pls.operations.append(exists)

    if exists.error:
        return pls

    if exists.data:
        return update_flow(client=db_client, track=track, pls=pls, row=exists.data)

    inserted = insert_flow(client=db_client, track=track, pls=pls)

    if not inserted:
        return pls

    pls.status = Status.COMPLETED
    return pls


def main():
    """Runs the flow"""
    while True:
        pls = main_flow()
        pls.log_status(logger=logger)
        sleep(30)


if __name__ == "__main__":
    main()
