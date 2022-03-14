"""Main flow"""

from datetime import datetime, timedelta
from typing import Tuple

from clients.secret_manager import SecretManager
from clients.spotify import init_spotify_client
from clients.postgres import PostgresClient
from tasks.spotify import get_current_track
from tasks.db import (
    check_exists,
    insert_album,
    insert_artist,
    insert_track,
    count_new_track,
    update_track_count,
)

from prefect import Flow, case  # pyright: reportPrivateImportUsage=false
from prefect.schedules import IntervalSchedule
from spotipy import Spotify


SCHEDULE = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1),
    interval=timedelta(seconds=30),
)


def build_flow(spotify_client: Spotify, db_client: PostgresClient) -> Flow:
    """Builds the prefect flow

    Returns:
        Flow: _description_
    """
    with Flow("datafy", schedule=SCHEDULE) as flow:
        track = get_current_track(client=spotify_client)

        # pylint: disable=no-member
        exists = check_exists(
            client=db_client,
            track=track,
        ).set_upstream(task=track)

        with case(exists, False):
            inserted_album = insert_album(client=db_client, track=track)
            inserted_artist = insert_artist(client=db_client, track=track)
            # pylint: disable=no-member
            inserted_track = (
                insert_track(
                    client=db_client,
                    track=track,
                )
                .set_upstream(task=inserted_album)
                .set_upstream(task=inserted_artist)
            )

            # pylint: disable=no-member
            count_new_track(
                client=db_client,
                track=track,
            ).set_upstream(task=inserted_track)

        with case(exists, True):
            update_track_count(client=db_client, track=track)

    return flow


def init_clients() -> Tuple[Spotify, PostgresClient]:
    """Initializes various application clients"""
    sm_client = SecretManager()
    spotify_client = init_spotify_client(sm_client=sm_client)
    db_client = PostgresClient(sm_client=sm_client)

    return spotify_client, db_client


def main():
    """Runs the flow"""
    spotify_client, db_client = init_clients()
    flow = build_flow(spotify_client=spotify_client, db_client=db_client)
    # flow.visualize()
    flow.run()


if __name__ == "__main__":
    main()
