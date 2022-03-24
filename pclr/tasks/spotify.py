from typing import Union

from spotipy import Spotify

from models.track import Track
from telemetry.logging import logger

LAST_PLAYED = {"id": ""}


def get_current_track(client: Spotify) -> Union[Track, None]:
    """Task to get the current track from Spotify. Raises a SKIP signal
    if no track is playing.
    """
    logger.info("Retrieving current playing track")

    response = client.current_user_playing_track()
    if not response:
        logger.info("No track currently playing")
        return None

    track = Track.from_dict(response)
    logger.info(
        "Currently playing",
        track_id=track.track_id,
        progress_pct=f"{track.progress_pct:.1f}%",
    )

    if LAST_PLAYED["id"] == track.track_id:
        logger.info(
            "Current track same as last track - skipping", track_id=track.track_id
        )
        return None

    LAST_PLAYED["id"] = track.track_id
    return track