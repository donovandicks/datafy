"""Main code for the newsletter"""

from datetime import datetime

from aws import Dynamo
from boto3.dynamodb.conditions import Key
from telemetry.logging import logger


class Newsletter:
    """Class containing methods for the newsletter"""

    def __init__(self, dynamo_client: Dynamo) -> None:
        self.__dynamo = dynamo_client

    def scan_table(self, table_name: str):
        """
        Scans the Spotify Tracks Table for play count
        """
        items = self.__dynamo.scan_table(
            table_name=table_name,
            filter_expr=Key("last_played_on").lte(str(datetime.now())),
        )
