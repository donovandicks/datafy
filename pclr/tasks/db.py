"""Tasks related to interacting with the Database"""
from typing import List

from clients.postgres import PostgresClient
from models.db import Artist, Album, PlayCount, Track
from models.ops import Status, PipelineStatus, Task
from models.track import CurrentlyPlaying
from telemetry.logging import logger


def insert_album(client: PostgresClient, track: CurrentlyPlaying) -> Task[bool]:
    """Inserts an album"""
    logger.info("Inserting new album", album_id=track.album_id)
    task = Task(status=Status.NONE, name="insert_album")
    album_exists = client.check_exists(table=Album, key=Album.id, value=track.album_id)
    if album_exists:
        logger.info(
            "Skipping album insertion - already exists", album_id=track.album_id
        )
        return task.with_status(Status.COMPLETED).with_data(True)

    album = Album.from_spotify(track)

    try:
        client.insert(item=album)
    except Exception as ex:
        logger.error("Failed to insert album", error=str(ex).strip())
        return task.with_status(Status.FAILED).with_error(ex).with_data(False)

    return task.with_status(Status.COMPLETED).with_data(True)


def insert_artist(client: PostgresClient, track: CurrentlyPlaying) -> Task[bool]:
    """Inserts an artist"""
    logger.info("Inserting new artist", artist_id=track.artist_id)
    task = Task(status=Status.NONE, name="insert_artist")
    artist_exists = client.check_exists(
        table=Artist, key=Artist.id, value=track.artist_id
    )
    if artist_exists:
        logger.info(
            "Skipping artist insertion - already exists", artist_id=track.artist_id
        )
        return task.with_status(Status.COMPLETED).with_data(True)

    artist = Artist.from_spotify(item=track)

    try:
        client.insert(artist)
    except Exception as ex:
        logger.error(
            "Failed to insert artist", artist_id=track.artist_id, error=str(ex).strip()
        )
        return task.with_status(Status.FAILED).with_error(ex).with_data(False)

    return task.with_status(Status.COMPLETED).with_data(True)


def insert_track(client: PostgresClient, track: CurrentlyPlaying) -> Task[bool]:
    """Inserts a track"""
    logger.info("Inserting new track", track_id=track.track_id)
    task = Task(status=Status.NONE, name="insert_track")
    track_exists = client.check_exists(table=Track, key=Track.id, value=track.track_id)
    if track_exists:
        logger.info(
            "Skipping track insertion - already exists", track_id=track.track_id
        )
        return task.with_status(Status.COMPLETED).with_data(True)

    track_db = Track.from_spotify(item=track)

    try:
        client.insert(item=track_db)
    except Exception as ex:
        logger.error(
            "Failed to insert track", track_id=track.track_id, error=str(ex).strip()
        )
        return task.with_status(Status.FAILED).with_error(ex).with_data(False)

    return task.with_status(Status.COMPLETED).with_data(True)


def count_new_track(client: PostgresClient, track: CurrentlyPlaying) -> Task[bool]:
    """Inserts a play count record"""
    logger.info("Counting play for new track", track_id=track.track_id)
    task = Task(status=Status.NONE, name="count_new_track")
    play_count = PlayCount(
        id=track.track_id,
        last_played_timestamp=track.timestamp,
        total_play_count=1,
    )

    try:
        client.insert(play_count)
    except Exception as ex:
        logger.error(
            "Failed to count new track", track_id=track.track_id, error=str(ex).strip()
        )
        return task.with_status(Status.FAILED).with_error(ex).with_data(False)

    return task.with_status(Status.COMPLETED).with_data(True)


def update_track_count(
    client: PostgresClient, track: CurrentlyPlaying, row: PlayCount
) -> Task[bool]:
    """Updates the play count for an existing track"""
    logger.info("Updating play count for existing track", track_id=track.track_id)
    task = Task(status=Status.NONE, name="update_track_count")

    try:
        client.update(
            table=PlayCount,
            filter_key=PlayCount.id,
            filter_value=track.track_id,
            update_key="total_play_count",
            update_value=row.total_play_count + 1,
        )
    except Exception as ex:
        logger.error(
            "Failed to update count for track",
            track_id=track.track_id,
            error=str(ex).strip(),
        )
        return task.with_status(Status.FAILED).with_error(ex).with_data(False)

    return task.with_status(Status.COMPLETED).with_data(True)


def check_counted(
    client: PostgresClient, track: CurrentlyPlaying
) -> Task[List[PlayCount]]:
    """Checks for an existing track"""
    task = Task(status=Status.NONE, name="check_counted")
    try:
        results = client.get_row(
            table=PlayCount, key=PlayCount.id, value=track.track_id
        )
        return task.with_status(Status.COMPLETED).with_data(results)
    except Exception as ex:
        return task.with_status(Status.FAILED).with_error(ex)


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
