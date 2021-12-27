"""Code for interacting with Spotify"""

import logging
from json import loads
from os import environ

from boto3 import resource, session
from botocore.exceptions import ClientError
from models.track import Track
from spotipy import Spotify, SpotifyOAuth

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_sm_error(err_obj: ClientError, sec_name: str) -> str:
    """
    Parses a secret manager error into a useful log string

    Params
    ------
    err_obj: ClientError
        the original error object
    sec_name: str
        the name of the secret that was being retrieved
    """
    err_code = err_obj.response["Error"]["Code"]
    if err_code == "ResourceNotFoundException":
        return f"The secret {sec_name} was not found"
    elif err_code == "InvalidRequestException":
        return f"The secret request was invalid: {err_obj}"
    elif err_code == "DecryptionFailure":
        return f"The secret cannot be decrypted: {err_obj}"
    elif err_code == "InternalServiceErrorException":
        return f"An error occurred on AWS server side: {err_obj}"
    else:
        return f"An unexpected error occurred retrieving secret {sec_name}: {err_obj}"


class Client:
    """The Spotiy client wrapper"""

    def __init__(self) -> None:
        self.__boto3_session = session.Session()
        self.__dynamo_client = resource(
            "dynamodb",
            region_name=environ["REGION_NAME"],
        )

        self.dyn_table = self.__dynamo_client.Table(environ["SPOTIFY_TRACKS_TABLE"])
        self.sm_client = self.__boto3_session.client(
            service_name="secretsmanager",
            region_name=environ["REGION_NAME"],
        )

        self.client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.__get_secret(environ["CLIENT_ID_KEY"]),
                client_secret=self.__get_secret(environ["CLIENT_SECRET_KEY"]),
                redirect_uri="http://localhost:8080",
                scope=environ["API_SCOPE"],
            )
        )

    def __get_secret(self, sec_name: str) -> str:
        """
        Retrieves a secret from AWS secret manager

        Params
        ------
        sec_name: str
            the name of the secret in AWS SM

        Returns
        _______
        secret: str
            the secret retrieved from AWS
        """
        try:
            secrets = self.sm_client.get_secret_value(
                SecretId=environ["SPOTIFY_SECRETS"]
            ).get("SecretString")
            return loads(secrets)[sec_name]

        except ClientError as ex:
            logger.exception(parse_sm_error(ex, sec_name))
            raise ex

    def update_track(self, track: Track) -> None:
        """
        Updates a track in DynamoDB by incrementing play count value

        Params
        ------
        track: Track
            a `Track` object to update information for
        """
        existing = self.dyn_table.get_item(
            Key={"track_id": track.id},
            ProjectionExpression="play_count",
        )

        if "Item" not in existing:
            logger.info("Track %s is not being counted - inserting", track.id)
            self.dyn_table.put_item(
                Item={
                    "track_id": track.id,
                    "track_name": track.name,
                    "play_count": 1,
                },
                ReturnValues="ALL_OLD",
            )
            return

        current_play_count = int(existing.get("Item", "").get("play_count", 0))
        logger.info(
            "Track %s currently has %i plays - incrementing",
            track.id,
            current_play_count,
        )

        self.dyn_table.update_item(
            Key={"track_id": track.id},
            UpdateExpression="SET play_count = play_count + :c",
            ExpressionAttributeValues={
                ":c": 1,
            },
            ReturnValues="UPDATED_NEW",
        )
        logger.info(
            "Updated track %s to play count %i", track.id, current_play_count + 1
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
        current_track = self.client.current_user_playing_track()
        if not current_track:
            return None

        track = Track.from_dict(current_track)
        logger.info("Currently playing %s", track.name)

        self.update_track(track)
        return track
