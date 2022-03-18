from typing import Union

from models.track import Track

from spotipy import Spotify

import prefect
from prefect import task


logger = prefect.logging.get_logger(__name__)

LAST_PLAYED = {"id": ""}


@task
def get_current_track(client: Spotify) -> Union[Track, None]:
    """Task to get the current track from Spotify. Raises a SKIP signal
    if no track is playing.
    """
    logger.info("Retrieving current track.")

    response = client.current_user_playing_track()
    if not response:
        logger.info("Not currently playing.")
        return None

    track = Track.from_dict(response)

    if LAST_PLAYED["id"] == track.track_id:
        logger.info(f"Still playing song {track.track_id}")
        return None

    LAST_PLAYED["id"] = track.track_id
    logger.info(f"Currently Playing: {track}")
    return track
