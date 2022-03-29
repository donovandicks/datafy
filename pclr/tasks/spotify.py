from typing import Union

from spotipy import Spotify

from models.ops import Status, PipelineStatus, Task
from models.track import CurrentlyPlaying
from telemetry.logging import logger

LAST_PLAYED = {"id": ""}


def get_current_track(client: Spotify) -> Task[CurrentlyPlaying]:
    """Task to get the current track from Spotify."""
    logger.info("Retrieving current playing track")
    task = Task(status=Status.NONE, name="get_current_track")
    response = client.current_user_playing_track()
    if not response:
        logger.info("No track currently playing")
        return task.with_status(Status.NO_CONTENT)

    track = CurrentlyPlaying.from_dict(response)
    logger.info(
        "Currently playing",
        track_id=track.track_id,
        progress_pct=track.progress_pct,
    )
    return task.with_status(Status.COMPLETED).with_data(track)


def check_last_played(track: CurrentlyPlaying) -> Task[bool]:
    """

    Returns
    -------
    Task[bool]:
        status: NOT_APPLICABLE | COMPLETED
        data: bool
            True if the current song was last played
    """
    task = Task(status=Status.NONE, name="check_last_played")
    if LAST_PLAYED.get("id", "") == track.track_id:
        logger.info(
            "Current track same as last track - skipping", track_id=track.track_id
        )
        return task.with_status(Status.NOT_APPLICABLE).with_data(True)

    LAST_PLAYED["id"] = track.track_id
    return task.with_status(Status.COMPLETED).with_data(False)


def spotify_flow(
    client: Spotify, pls: PipelineStatus
) -> Union[PipelineStatus, CurrentlyPlaying]:
    track_task = get_current_track(client=client)
    pls.operations.append(track_task)
    if not track_task.data:
        return pls.with_status(status=Status.COMPLETED)

    was_last_played = check_last_played(track=track_task.data)
    pls.operations.append(was_last_played)
    if was_last_played.data:
        return pls.with_status(status=Status.COMPLETED)

    return track_task.data
