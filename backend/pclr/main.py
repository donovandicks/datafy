"""Main flow"""
from time import sleep
from typing import Tuple

from clients.secret_manager import SecretManager
from clients.spotify import init_spotify_client
from clients.postgres import PostgresClient
from tasks.spotify import get_current_track
from tasks.db import (
    check_counted,
    insert_album,
    insert_artist,
    insert_track,
    count_new_track,
    update_track_count,
)

from prefect import flow
from spotipy import Spotify


def init_clients() -> Tuple[Spotify, PostgresClient]:
    """Initializes various application clients"""
    sm_client = SecretManager()
    spotify_client = init_spotify_client(sm_client=sm_client)
    database_client = PostgresClient(sm_client=sm_client)
    return spotify_client, database_client


sp_client, db_client = init_clients()


@flow
def main_flow():
    """Main flow"""
    track = get_current_track(client=sp_client).wait().result()

    if not track:
        return

    exists = check_counted(client=db_client, track=track).wait().result()

    if exists:
        update_track_count(client=db_client, track=track)
        return

    inserted_album = insert_album(client=db_client, track=track).wait().result()
    inserted_artist = insert_artist(client=db_client, track=track).wait().result()

    if not inserted_album or not inserted_artist:
        return

    inserted_track = insert_track(client=db_client, track=track).wait().result()

    if not inserted_track:
        return

    count_new_track(client=db_client, track=track)


if __name__ == "__main__":
    while True:
        main_flow()
        sleep(30)
