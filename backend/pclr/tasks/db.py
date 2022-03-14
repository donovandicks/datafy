"""Tasks related to interacting with the Database"""
from typing import Union

from clients.postgres import PostgresClient
from models.db import FilterExpression, UpdateClause
from models.track import Track
from prefect.triggers import all_successful
from prefect.utilities.tasks import task
from prefect.utilities.context import context

logger = context.get("logger")


@task
def insert_album(client: PostgresClient, track: Union[Track, None]) -> bool:
    """Inserts an album"""
    if not track:
        logger.info("No album to insert")
        return False

    logger.info(f"Inserting album {track.album_id}")

    values = (
        track.album_id,
        track.album_name,
    )

    client.insert(table="album", values=values)
    return True


@task
def insert_artist(client: PostgresClient, track: Union[Track, None]) -> bool:
    """Inserts an artist"""
    if not track:
        logger.info("No artist to insert")
        return False

    logger.info(f"Inserting artist {track.artist_id}")

    values = (
        track.artist_id,
        track.artist_name,
    )

    client.insert(table="artist", values=values)
    return True


@task
def insert_track(client: PostgresClient, track: Union[Track, None]) -> bool:
    """Inserts a track"""
    if not track:
        logger.info("No track to insert")
        return False

    logger.info(f"Inserting track {track.track_id}")

    values = (
        track.track_id,
        track.track_name,
        track.artist_id,
        track.album_id,
    )

    client.insert(table="track", values=values)
    return True


@task
def count_new_track(client: PostgresClient, track: Union[Track, None]) -> bool:
    """Inserts a play count record"""
    if not track:
        logger.info("No track to count")
        return False

    logger.info(f"Counting play for track {track.track_id}")

    values = (
        track.track_id,
        track.timestamp,
        1,
    )

    client.insert(table="play_count", values=values)
    return True


@task
def update_track_count(client: PostgresClient, track: Union[Track, None]) -> bool:
    """Updates the play count for an existing track"""
    if not track:
        logger.info("No track to update")
        return False

    logger.info(f"Updated play count for {track.track_id}")

    update = UpdateClause(
        update_field="total_play_count",
        update_value="total_play_count + 1",
        filter_expr=FilterExpression(
            filter_field="track_id",
            filter_condition="=",
            filter_value=track.track_id,
        ),
    )

    client.update(table="play_count", clause=update)
    return True


@task
def check_exists(client: PostgresClient, track: Union[Track, None]) -> bool:
    """Checks for an existing track"""
    if not track:
        logger.info("No track to search for")
        return False

    filter_expr = FilterExpression(
        filter_field="track_id",
        filter_condition="=",
        filter_value=track.track_id,
    )

    result = client.get_row(table="play_count", filter_expr=filter_expr)
    logger.info(
        f"Retrieved database item where {filter_expr.build_filter_expression()}: {result}"
    )

    return bool(result)


@task(trigger=all_successful)
def view_database(client: PostgresClient):
    """Shows existing data in the db"""
    logger.info("Retrieving all data from the database")
    records = client.get_all_rows(table="play_count")
    logger.info(f"Retrieved records: {records}")
