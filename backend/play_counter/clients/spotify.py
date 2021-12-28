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
                scope=environ["API_SCOPES"],
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
            table_name=environ["SPOTIFY_TRACKS_TABLE"],
            key_name="track_id",
            key_val=track.id,
            attributes=["play_count"],
        )

        last_played = self.aws_client.get_dynamo_item(
            table_name=environ["SPOTIFY_CACHE_TABLE"],
            key_name="key",
            key_val="last_played",
            attributes=["val"],
        )

        if "Item" not in existing:
            logger.info(
                "Inserting new uncounted track",
                track_id=track.id,
                track_name=track.name,
            )
            self.aws_client.insert_dynamo_item(
                table_name=environ["SPOTIFY_TRACKS_TABLE"],
                item={
                    "track_id": track.id,
                    "track_name": track.name,
                    "play_count": 1,
                },
            )
            self.aws_client.insert_dynamo_item(
                table_name=environ["SPOTIFY_CACHE_TABLE"],
                item={"key": "last_played", "val": track.id},
            )
            return

        if last_played.get("Item", {}).get("val", "") == track.id:
            logger.info(
                "Skipping Update",
                track_id=track.id,
                track_name=track.name,
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
            table_name=environ["SPOTIFY_TRACKS_TABLE"],
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
        currently_playing = self.spotify_client.current_user_playing_track()

        if not currently_playing:
            logger.info("Currently Playing", track_name="None")
            return None

        current_track = Track.from_dict(currently_playing)
        logger.info("Currently Playing", track_name=current_track.name)

        self.update_track(current_track)
        return current_track
