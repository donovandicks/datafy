"""Tasks related to interacting with the Database"""
from typing import List

from clients.postgres import PostgresClient
from models.db import PlayCount
from models.ops import Status, Task
from models.track import CurrentlyPlaying
from telemetry.logging import logger


def count_new_track(client: PostgresClient, track: CurrentlyPlaying) -> Task[bool]:
    """Inserts a play count record"""
    logger.info("Counting play for new track", track_id=track.track_id)
    task = Task(status=Status.NONE, name="count_new_track")
    play_count = PlayCount(
        track_id=track.track_id,
        last_played_timestamp=track.timestamp,
        total_play_count=1,
    )

    try:
        client.insert(play_count)
        return task.with_status(Status.COMPLETED).with_data(True)
    except Exception as ex:
        logger.error(
            "Failed to count new track", track_id=track.track_id, error=str(ex).strip()
        )
        return task.with_status(Status.FAILED).with_error(ex).with_data(False)


def update_track_count(
    client: PostgresClient, track: CurrentlyPlaying, row: PlayCount
) -> Task[bool]:
    """Updates the play count for an existing track"""
    logger.info("Updating play count for existing track", track_id=track.track_id)
    task = Task(status=Status.NONE, name="update_track_count")

    try:
        client.update(
            table=PlayCount,
            filter_key=PlayCount.track_id,
            filter_value=track.track_id,
            update_key="total_play_count",
            update_value=row.total_play_count + 1,
        )
        return task.with_status(Status.COMPLETED).with_data(True)
    except Exception as ex:
        logger.error(
            "Failed to update count for track",
            track_id=track.track_id,
            error=str(ex).strip(),
        )
        return task.with_status(Status.FAILED).with_error(ex).with_data(False)


def check_counted(
    client: PostgresClient, track: CurrentlyPlaying
) -> Task[List[PlayCount]]:
    """Checks for an existing track"""
    task = Task(status=Status.NONE, name="check_counted")
    try:
        results = client.get_row(
            table=PlayCount, key=PlayCount.track_id, value=track.track_id
        )
        return task.with_status(Status.COMPLETED).with_data(results)
    except Exception as ex:
        logger.error(
            "Failed to check for counted track",
            track_id=track.track_id,
            error=str(ex).strip(),
        )
        return task.with_status(Status.FAILED).with_error(ex)
