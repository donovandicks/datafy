"""Contains wrapper code for SQS"""

from boto3 import client
from botocore.exceptions import ClientError
from telemetry.logging import logger


class SQS:
    """
    Client wrapper for AWS SQS
    """

    def __init__(self) -> None:
        self.__client = client("sqs")

    def send_message(self, queue_url: str, msg: str):
        """Sends a message to an sqs queue

        Params
        ------
        queue_url: str
            the message queue to deliver messages to
        msg: str
            the message to be sent to the queue
        """
        try:
            res = self.__client.send_message(
                QueueUrl=queue_url,
                MessageBody=msg,
            )

            logger.info(
                "Successfully queued message",
                queue=queue_url,
                message_id=res.get("MessageId", ""),
            )
        except ClientError as ex:
            logger.error("Failed to send message to queue", queue=queue_url)
            raise ex
