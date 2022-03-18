"""Tasks related to interacting with the Database"""
from clients.postgres import PostgresClient
from domain.common import check_exists
from models.db import FilterExpression, UpdateClause
from models.track import Track

import prefect
from prefect import task

logger = prefect.logging.get_logger(__name__)


@task
def insert_album(client: PostgresClient, track: Track) -> bool:
    """Inserts an album"""
    album_exists = check_exists(client=client, track=track, item="album")
    if album_exists:
        return True

    logger.info(f"Inserting album {track.album_id}")

    values = (
        track.album_id,
        track.album_name,
    )

    try:
        client.insert(table="album", values=values)
    except Exception as ex:
        logger.error(f"Failed to insert album {track.album_id}")
        return False

    return True


@task
def insert_artist(client: PostgresClient, track: Track) -> bool:
    """Inserts an artist"""
    artist_exists = check_exists(client=client, track=track, item="artist")
    if artist_exists:
        return True

    logger.info(f"Inserting artist {track.artist_id}")

    values = (
        track.artist_id,
        track.artist_name,
    )

    try:
        client.insert(table="artist", values=values)
    except Exception as ex:
        logger.error(f"Failed to insert artist {track.artist_id}: {ex}")
        return False

    return True


@task
def insert_track(client: PostgresClient, track: Track) -> bool:
    """Inserts a track"""
    track_exists = check_exists(client=client, track=track, item="track")
    if track_exists:
        return True

    logger.info(f"Inserting track {track.track_id}")

    values = (
        track.track_id,
        track.track_name,
        track.artist_id,
        track.album_id,
    )

    try:
        client.insert(table="track", values=values)
    except Exception as ex:
        logger.error(f"Failed insert track {track.track_id}: {ex}")
        return False

    return True


@task
def count_new_track(client: PostgresClient, track: Track) -> bool:
    """Inserts a play count record"""
    logger.info(f"Counting play for track {track.track_id}")

    values = (
        track.track_id,
        track.timestamp,
        1,
    )

    client.insert(table="play_count", values=values)
    return True


@task
def update_track_count(client: PostgresClient, track: Track) -> bool:
    """Updates the play count for an existing track"""
    logger.info(f"Updating play count for {track.track_id}")

    update = UpdateClause(
        update_field="total_play_count",
        update_value="total_play_count + 1",
        filter_expr=FilterExpression(
            filter_field="track_id",
            filter_condition="=",
            filter_value=track.track_id,
        ),
    )

    try:
        client.update(table="play_count", clause=update)
    except Exception as ex:
        logger.error(f"Failed to update play count for {track.track_id}: {ex}")
        return False

    return True


@task
def check_counted(client: PostgresClient, track: Track) -> bool:
    """Checks for an existing track"""
    logger.info(f"Checking if track {track.track_id} is being counted")
    return check_exists(client=client, track=track, item="play_count")


@task
def view_database(client: PostgresClient):
    """Shows existing data in the db"""
    logger.info("Retrieving all data from the database")
    records = client.get_all_rows(table="play_count")
    logger.info(f"Retrieved records: {records}")
