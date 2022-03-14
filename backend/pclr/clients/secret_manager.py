"""Code for interacting with AWS"""

from json import loads
import os
from typing import Dict

from models.result import Result

from boto3 import session
from botocore.exceptions import ClientError, NoCredentialsError


def parse_sm_error(err_obj: ClientError, sec_id: str) -> str:
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
        "ResourceNotFoundException": f"The secret {sec_id} was not found",
        "InvalidRequestException": f"The secret request was invalid: {err_obj}",
        "DecryptionFailure": f"The secret cannot be decrypted: {err_obj}",
        "InternalServiceErrorException": f"An error occurred on AWS server side: {err_obj}",
    }

    if err_code in err_msgs:
        return err_msgs[err_code]

    return f"An unexpected error occurred retrieving secret {sec_id}: {err_obj}"


class SecretManager:
    """Wrapper for AWS SecretManager"""

    def __init__(self) -> None:
        self.__boto3_session = session.Session()

        self.sm_client = self.__boto3_session.client(
            service_name="secretsmanager",
            region_name=os.environ.get("REGION_NAME", "us-east-1"),
        )

    def get_secret(self, sec_id: str, sec_name: str) -> Result[str]:
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
        print(f"Attempting to retrieve secret {sec_name} from {sec_id}")
        secrets = self.get_secrets(sec_id=sec_id)

        if secrets.value:
            return Result(
                value=secrets.value.get(sec_name, ""),
                error=None,
            )

        return Result(
            value=None,
            error=secrets.error,
        )

    def get_secrets(self, sec_id: str) -> Result[Dict]:
        """Retrieves the secrets under the specified ID"""
        try:
            print(f"Attempting to retrieve secrets under {sec_id}")
            secrets = self.sm_client.get_secret_value(SecretId=sec_id).get(
                "SecretString"
            )
            return Result(
                value=loads(secrets),
                error=None,
            )

        except ClientError as ex:
            return Result(
                value=None,
                error=parse_sm_error(err_obj=ex, sec_id=sec_id),
            )

        except NoCredentialsError as ex:
            return Result(
                value=None,
                error=str(ex),
            )
