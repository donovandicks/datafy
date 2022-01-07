"""Code for AWS Simple Email Service"""

from boto3 import client
from botocore.exceptions import ClientError
from telemetry.logging import logger

from .models.email import Email


class SES:
    """Wrapper for AWS SES"""

    def __init__(self) -> None:
        self.__client = client("ses")

    def send_email(self, email: Email):
        """
        Attempt to send the given email

        Params
        ------
        email: Email
            an Email data model containing the metadata and data for the actual email
            to be sent to a user
        """
        try:
            self.__client.send_email(**email.to_dict())
        except ClientError as ex:
            logger.error("Failed to Send Report", error=ex)
            raise ex
