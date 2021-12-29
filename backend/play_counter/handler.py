"""Main entry point for the play-counter lambda"""
from os import environ

from botocore.exceptions import ClientError
from structlog import get_logger

from clients.aws import AWS
from clients.spotify import SpotifyClient
from models.lambda_state import LambdaAction
from telemetry.logging import Logger

log_client = get_logger(__name__)
logger = Logger(logger=log_client)


def run(_, context):
    """
    The lambda handler called on function execution

    _:
        the event received on function execution
    context:
        the lambda function metadata
    """
    logger.log_execution(context.function_name, LambdaAction.TRIGGERED)
    eb_rule = environ["EVENT_BRIDGE_RULE"]
    aws_client = AWS()
    sp_client = SpotifyClient(aws_client=aws_client)

    try:
        current_rule_schedule = aws_client.get_rule_schedule(name=eb_rule)
        current_song = sp_client.get_current_song()

        if not current_song and (current_rule_schedule != "rate(5 minutes)"):
            aws_client.update_event_rule(name=eb_rule, rate=5)
            return

        if current_song and (current_rule_schedule == "rate(5 minutes)"):
            aws_client.update_event_rule(name=eb_rule, rate=1)

    except ClientError as ex:
        logger.log_failure(context.function_name, ex)

    logger.log_execution(context.function_name, LambdaAction.COMPLETED)
