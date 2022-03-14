from models.track import Track

from spotipy import Spotify

import prefect
from prefect import task  # pyright: reportPrivateImportUsage=false
from prefect.engine.signals import SKIP

logger = prefect.context.get("logger")  # pyright: reportPrivateImportUsage=false

LAST_PLAYED = {"id": ""}


@task
def get_current_track(client: Spotify):
    """Task to get the current track from Spotify. Raises a SKIP signal
    if no track is playing.
    """
    logger.info("Retrieving current track.")

    response = client.current_user_playing_track()
    if not response:
        logger.info("Not currently playing.")
        raise SKIP()

    track = Track.from_dict(response)

    if LAST_PLAYED["id"] == track.track_id:
        logger.info(f"Still playing song {track.track_id}")
        raise SKIP()

    LAST_PLAYED["id"] = track.track_id
    logger.info(f"Currently Playing: {track}")
    return track


@task
def check_last_played(track: Track):
    """Checks if the current playing song is the same as the last played.
    Raises a SKIP signal if they are the same to exit the flow early.
    """
    if track.track_id == LAST_PLAYED["id"]:
        raise SKIP()

    return True
