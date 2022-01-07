"""Code for working with EventBridge"""

from boto3 import client
from botocore.exceptions import ClientError
from telemetry.logging import logger


class EventBridge:
    """Wrapper for AWS EventBridge"""

    def __init__(self) -> None:
        self.__client = client("events")

    def get_event_rule(self, name: str) -> dict:
        """
        Retrieves details about an EventBridge rule

        Params
        ------
        name: str
            the name of the rule to retrieve

        Returns
        -------
        an object containing information about the EventBridge rule

        Raises
        ------
        `ClientError` if an error is encountered when retrieving the rule from AWS
        """
        logger.info("Retrieving EventBridge Rule", name=name)
        try:
            rule = self.__client.describe_rule(Name=name)
            return rule
        except ClientError as ex:
            logger.error(
                "Failed to retrieve EventBridge Rule", rule_name=name, error=str(ex)
            )
            raise ex

    def get_rule_schedule(self, name: str) -> str:
        """
        Retrieves the schedule for the rule with the given name

        Params
        ------
        name: str
            the name of the EventBridge rule to retrieve the schedule for

        Returns
        -------
        the schedule expression of the rule
        """
        logger.info("Retrieving EventBridge Rule Schedule", rule_name=name)
        return self.get_event_rule(name=name).get("ScheduleExpression", "")

    def update_event_rule(self, name: str, rate: int, period: str):
        """
        Updates an EventBridge rule

        Params
        ------
        rate: int
            the number of `period`s to pass before triggering the event again
        period: str
            the time period to pass (minute, hour, etc.)
        """
        assert rate >= 1

        logger.info("Updating EventBridge Rule", name=name, rate=rate)
        expression = f"rate({rate} {period})"
        self.__client.put_rule(
            Name=name,
            ScheduleExpression=expression,
        )
