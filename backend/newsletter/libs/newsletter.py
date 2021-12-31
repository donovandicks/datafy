"""Main code for the newsletter"""

from datetime import datetime, timedelta
from os import environ

from aws import Dynamo
from boto3.dynamodb.conditions import Key
from telemetry.logging import logger


class Newsletter:
    """Class containing methods for the newsletter"""

    def __init__(self, dynamo_client: Dynamo) -> None:
        self.__dynamo = dynamo_client
        self.__one_week_ago = datetime.now() - timedelta(days=7)
        self.__today = datetime.now()

    def get_last_count(self) -> int:
        """
        Retrieves the total play count as of 7 days ago
        """
        logger.info("Retrieving Last Total Count", as_of=str(self.__one_week_ago))

        cached_count = (
            self.__dynamo.get_item(
                table_name=environ["SPOTIFY_CACHE_TABLE"],
                key_name="key",
                key_val="total_count",
                attributes=["val"],
            )
            .get("Item", {})
            .get("val", 0)
        )

        if cached_count:
            logger.info(
                "Retrieved Cached Count",
                cached_count=cached_count,
                as_of=str(self.__one_week_ago),
            )
            return cached_count

        count = sum(
            [
                int(item["play_count"])
                for item in self.__dynamo.scan_table(
                    table_name=environ["SPOTIFY_TRACKS_TABLE"],
                    filter_expr=Key("last_played_timestamp").lte(
                        int(self.__one_week_ago.timestamp())
                    ),
                )
            ]
        )

        logger.info(
            "Calculated Last Total Count", count=count, as_of=str(self.__one_week_ago)
        )
        return count

    def get_current_count(self) -> int:
        """
        Retrieves the current total play counts

        Returns
        -------
        count: int
            the total number of plays for all tracks in the database
        """
        count = sum(
            [
                int(item["play_count"])
                for item in self.__dynamo.scan_table(
                    table_name=environ["SPOTIFY_TRACKS_TABLE"],
                )
            ]
        )

        logger.info("Total Current Plays", count=count, as_of=str(self.__today))
        return count

    def get_new_count(self) -> int:
        """
        Calculates the number of plays added in the last week
        """
        logger.info(
            "Calculating New Plays",
            since=str(self.__one_week_ago),
            as_of=str(self.__today),
        )

        last_count = self.get_last_count()
        current_count = self.get_current_count()
        new_plays = current_count - last_count

        logger.info(
            "Calculated New Plays",
            new_plays=new_plays,
            current_count=current_count,
            last_count=last_count,
        )
        return new_plays

    def create_report(self):
        """
        Generates a report to send to the user regarding the changes in their listening
        habits over the last week
        """
        logger.info(
            "Generating Listening Report",
            week_beginning=str(self.__one_week_ago),
            week_ending=str(self.__today),
        )
        new_plays = self.get_new_count()
