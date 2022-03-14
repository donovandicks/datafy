"""Code for interacting with Spotify"""

import os

from clients.secret_manager import SecretManager

from dotenv import load_dotenv
from spotipy import Spotify, SpotifyOAuth

load_dotenv()


def init_spotify_client(sm_client: SecretManager) -> Spotify:
    """Initializes the Spotify client

    Returns:
        Spotify: _description_
    """
    spotify_secrets_id = os.environ.get("SPOTIFY_SECRETS_ID", "")
    secrets = {}

    response = sm_client.get_secrets(sec_id=spotify_secrets_id)
    if not response.value:
        raise Exception(f"Failed to retrieve Spotify secrets: {response.error}")

    for secret_name in ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET"]:
        secret_key = os.environ.get(secret_name, "")
        if not secret_key:
            raise KeyError(
                f"Unable to find secret identifier with name {secret_name} in the environment"
            )

        print(f"Retrieved secret {secret_name}")
        secrets[secret_name] = response.value.get(secret_key, "")

    return Spotify(
        auth_manager=SpotifyOAuth(
            client_id=secrets.get("SPOTIFY_CLIENT_ID", ""),
            client_secret=secrets.get("SPOTIFY_CLIENT_SECRET", ""),
            redirect_uri="http://localhost:8080",
            scope="user-read-currently-playing",
        )
    )
