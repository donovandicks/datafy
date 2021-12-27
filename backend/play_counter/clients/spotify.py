"""Code for interacting with Spotify"""

from os import environ

from models.track import Track
from spotipy import Spotify, SpotifyOAuth
from structlog import get_logger
from telemetry.logging import Logger

from .aws import AWS

log_client = get_logger(__name__)
logger = Logger(log_client)


class SpotifyClient:
    """The Spotiy client wrapper"""

    def __init__(self) -> None:
        self.aws_client = AWS()
        self.spotify_client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.aws_client.get_secret(environ["CLIENT_ID_KEY"]),
                client_secret=self.aws_client.get_secret(environ["CLIENT_SECRET_KEY"]),
                redirect_uri="http://localhost:8080",
                scope=environ["API_SCOPE"],
            )
        )

    def update_track(self, track: Track) -> None:
        """
        Updates a track in DynamoDB by incrementing play count value

        Params
        ------
        track: Track
            a `Track` object to update information for
        """
        existing = self.aws_client.get_dynamo_item(
            key_name="track_id",
            key_val=track.id,
            attributes=["play_count"],
        )

        if "Item" not in existing:
            logger.info(
                "Inserting new uncounted track",
                track_id=track.id,
                track_name=track.name,
            )
            self.aws_client.insert_dynamo_item(
                item={
                    "track_id": track.id,
                    "track_name": track.name,
                    "play_count": 1,
                },
            )
            return

        current_play_count = int(existing.get("Item", {}).get("play_count", 0))
        logger.info(
            "Incrementing counted track",
            track_id=track.id,
            track_name=track.name,
            current_plays=current_play_count,
        )

        self.aws_client.update_dynamo_item(
            key_name="track_id",
            key_val=track.id,
            update_expr="SET play_count = play_count + :c",
            expr_vals={
                ":c": 1,
            },
        )
        logger.info(
            "Updated counted track",
            track_id=track.id,
            track_name=track.name,
            new_plays=current_play_count + 1,
        )

    def get_current_song(self) -> Track | None:
        """
        Retrieves the current user's currently playing track

        Returns
        -------
        Track | None
            a `Track` object with the information from the currently playing song
            if the user is playing a song, otherwise `None`
        """
        # TODO: Refactor to reduce chances of returing `None`
        # Can accomplish by retrieving last played song if the user is not currently
        # playing a song. Does not encompass case where user has never played a
        # track. Unclear if there is a limit in lookback time as well.
        current_track = self.spotify_client.current_user_playing_track()
        if not current_track:
            logger.info("Currently Playing", track_name="None")
            return None

        track = Track.from_dict(current_track)
        logger.info("Currently Playing", track_name=track.name)

        self.update_track(track)
        return track
