"""Tasks related to interacting with AWS"""

import json

import prefect
from prefect import task  # pyright: reportPrivateImportUsage=false

from botocore.exceptions import ClientError


@task
def get_secret(sm_client, secret_name: str, secret_id: str):
    """Retrieves a secret"""
    logger = prefect.context.get("logger")
    logger.info(f"Retrieving secret {secret_name} from secret ID {secret_id}.")

    secret = ""
    try:
        secret_response = sm_client.get_secret_value(
            SecretId=secret_id,
        ).get("SecretString")
        secret = json.loads(secret_response).get(secret_name, "")
    except ClientError as ex:
        logger.error(f"Failed to retrieve secret {secret_name} from AWS: {ex}.")
        raise ex

    if not secret:
        msg = f"Unable to find secret {secret_name} on AWS response."
        logger.error(msg)
        raise KeyError(msg)

    logger.info(f"Successfully retrieved secret {secret_name} from AWS.")
    return secret
