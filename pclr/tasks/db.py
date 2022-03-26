"""Tasks related to interacting with the Database"""
from clients.postgres import PostgresClient
from domain.common import check_exists
from models.db import FilterExpression, UpdateClause
from models.track import Track
from telemetry.logging import logger


def insert_album(client: PostgresClient, track: Track) -> bool:
    """Inserts an album"""
    logger.info("Inserting new album", album_id=track.album_id)
    album_exists = check_exists(client=client, track=track, item="album")
    if album_exists:
        logger.info(
            "Skipping album insertion - already exists", album_id=track.album_id
        )
        return True

    values = (
        track.album_id,
        track.album_name,
    )

    try:
        client.insert(table="album", values=values)
    except Exception as ex:
        logger.error("Failed to insert album", exception=ex)
        return False

    return True


def insert_artist(client: PostgresClient, track: Track) -> bool:
    """Inserts an artist"""
    logger.info("Inserting new artist", artist_id=track.artist_id)
    artist_exists = check_exists(client=client, track=track, item="artist")
    if artist_exists:
        logger.info(
            "Skipping artist insertion - already exists", artist_id=track.artist_id
        )
        return True

    values = (
        track.artist_id,
        track.artist_name,
    )

    try:
        client.insert(table="artist", values=values)
    except Exception as ex:
        logger.error("Failed to insert artist", artist_id=track.artist_id)
        return False

    return True


def insert_track(client: PostgresClient, track: Track) -> bool:
    """Inserts a track"""
    logger.info("Inserting new track", track_id=track.track_id)
    track_exists = check_exists(client=client, track=track, item="track")
    if track_exists:
        logger.info(
            "Skipping track insertion - already exists", track_id=track.track_id
        )
        return True

    values = (
        track.track_id,
        track.track_name,
        track.artist_id,
        track.album_id,
        track.popularity,
    )

    try:
        client.insert(table="track", values=values)
    except Exception as ex:
        logger.error("Failed to insert track", track_id=track.track_id)
        return False

    return True


def count_new_track(client: PostgresClient, track: Track) -> bool:
    """Inserts a play count record"""
    logger.info("Counting play for new track", track_id=track.track_id)

    values = (
        track.track_id,
        track.timestamp,
        1,
    )

    client.insert(table="play_count", values=values)
    return True


def update_track_count(client: PostgresClient, track: Track) -> bool:
    """Updates the play count for an existing track"""
    logger.info("Updating play count for existing track", track_id=track.track_id)

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
        logger.error("Failed to update count for track", track_id=track.track_id)
        return False

    return True


def check_counted(client: PostgresClient, track: Track) -> bool:
    """Checks for an existing track"""
    return check_exists(client=client, track=track, item="play_count")


def view_database(client: PostgresClient):
    """Shows existing data in the db"""
    records = client.get_all_rows(table="play_count")
