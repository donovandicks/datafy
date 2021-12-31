"""Code for interacting with AWS"""

from json import loads
from os import environ

from boto3 import session
from botocore.exceptions import ClientError
from telemetry.logging import logger


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
    err_msgs = {
        "ResourceNotFoundException": f"The secret {sec_name} was not found",
        "InvalidRequestException": f"The secret request was invalid: {err_obj}",
        "DecryptionFailure": f"The secret cannot be decrypted: {err_obj}",
        "InternalServiceErrorException": f"An error occurred on AWS server side: {err_obj}",
    }

    if err_code in err_msgs:
        return err_msgs[err_code]

    return f"An unexpected error occurred retrieving secret {sec_name}: {err_obj}"


class SecretManager:
    """Wrapper for AWS SecretManager"""

    def __init__(self) -> None:
        self.__boto3_session = session.Session()

        self.sm_client = self.__boto3_session.client(
            service_name="secretsmanager",
            region_name=environ["REGION_NAME"],
        )

    def get_secret(self, sec_name: str) -> str:
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
            logger.error(
                "Failed to retrieve secret", error=parse_sm_error(ex, sec_name)
            )
            raise ex
