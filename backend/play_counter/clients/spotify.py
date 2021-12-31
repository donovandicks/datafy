"""Code for interacting with Spotify"""

from datetime import datetime
from os import environ
from typing import Union

from aws.dynamo import Dynamo
from aws.secretmanager import SecretManager
from models.track import Track
from spotipy import Spotify, SpotifyOAuth
from telemetry.logging import logger


class SpotifyClient:
    """The Spotiy client wrapper"""

    def __init__(self, dynamo_client: Dynamo, secret_manager: SecretManager) -> None:
        self.dynamo_client = dynamo_client
        self.secret_manager = secret_manager
        self.spotify_client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.secret_manager.get_secret(environ["CLIENT_ID_KEY"]),
                client_secret=self.secret_manager.get_secret(
                    environ["CLIENT_SECRET_KEY"]
                ),
                redirect_uri="http://localhost:8080",
                scope=environ["API_SCOPES"],
            )
        )

    def get_existing_track(self, track_id: str) -> dict:
        """
        Attempts to retrieve an existing track from dynamo

        Params
        ------
        track_id: str
            the track to look for

        Returns
        -------
        An object containing the play count of the existing track if it was found
        """
        return self.dynamo_client.get_dynamo_item(
            table_name=environ["SPOTIFY_TRACKS_TABLE"],
            key_name="track_id",
            key_val=track_id,
            attributes=["play_count"],
        )

    def get_last_played(self) -> dict:
        """
        Attempts to retrieve the last played track id from dynamo

        Returns
        -------
        An object containing the id of the last played song if one is found in
        the cache
        """
        return self.dynamo_client.get_dynamo_item(
            table_name=environ["SPOTIFY_CACHE_TABLE"],
            key_name="key",
            key_val="last_played",
            attributes=["val"],
        )

    def insert_cache_item(self, item: dict) -> None:
        """
        Inserts an item into the cache table

        Params
        ------
        item: dict
            the key-value pairs to be inserted into the cache table
        """
        logger.info("Inserting new cache item", item=str(item))
        self.dynamo_client.insert_dynamo_item(
            table_name=environ["SPOTIFY_CACHE_TABLE"], item=item
        )

    def insert_track(self, track: Track) -> None:
        """
        Inserts a track into the tracks table

        Params
        ------
        track: Track
            the `Track` object to add to the table
        """
        logger.info(
            "Inserting new uncounted track",
            track_id=track.id,
            track_name=track.name,
        )

        self.dynamo_client.insert_dynamo_item(
            table_name=environ["SPOTIFY_TRACKS_TABLE"],
            item={
                "track_id": track.id,
                "track_name": track.name,
                "play_count": 1,
                "last_played_on": str(datetime.now()),
            },
        )

    def update_track(self, track: Track, update_expr: str, expr_vals: dict) -> None:
        """
        Update a track in the database

        Params
        ------
        track: Track
            the `Track` object to update
        update_expr: str
            the keys being updated in the database
        expr_vals: dict
            a mapping to the `update_expr` with the values to update
        """
        logger.info("Updating existing track", track_id=track.id, track_name=track.name)

        self.dynamo_client.update_dynamo_item(
            table_name=environ["SPOTIFY_TRACKS_TABLE"],
            key_name="track_id",
            key_val=track.id,
            update_expr=update_expr,
            expr_vals=expr_vals,
        )

        logger.info("Updated existing track", track_id=track.id, track_name=track.name)

    def update_database(self, track: Track) -> None:
        """
        Updates a track in DynamoDB by incrementing play count value

        Params
        ------
        track: Track
            a `Track` object to update information for
        """
        existing = self.get_existing_track(track_id=track.id)
        last_played = self.get_last_played()

        if "Item" not in existing:
            self.insert_cache_item(item={"key": "last_played", "val": track.id})
            self.insert_track(track=track)
            return

        if last_played.get("Item", {}).get("val", "") == track.id:
            logger.info(
                "Skipping Update",
                track_id=track.id,
                track_name=track.name,
            )
            return

        self.insert_cache_item(item={"key": "last_played", "val": track.id})
        self.update_track(
            track=track,
            update_expr="SET play_count = play_count + :c, last_played_on = :d",
            expr_vals={":c": 1, ":d": str(datetime.now())},
        )

    def get_current_song(self) -> Union[Track, None]:
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
            logger.info("No Track Playing")
            return None

        current_track = Track.from_dict(currently_playing)
        logger.info("Currently Playing", track_name=current_track.name)

        self.update_database(current_track)
        return current_track
