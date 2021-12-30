"""Main entry point for the play-counter lambda"""
from datetime import datetime, time
from os import environ

from botocore.exceptions import ClientError

from clients.aws import AWS
from clients.spotify import SpotifyClient
from models.lambda_state import LambdaAction
from telemetry.logging import log_execution, log_failure, logger


def reschedule(aws_client: AWS, listening_now: bool):
    """
    Reschedules the EventBridge rule responsible for triggering this lambda

    Params
    ------
    aws_client: AWS
    listening_now: bool
    """
    eb_rule = environ["EVENT_BRIDGE_RULE"]
    current_rule_schedule = aws_client.get_rule_schedule(name=eb_rule)

    if (
        time.fromisoformat("02:00:00")
        < datetime.now().time()
        < time.fromisoformat("08:00:00")
    ) and (current_rule_schedule != "rate(1 hour)"):
        logger.info(
            "Rescheduling Execution", current=current_rule_schedule, new="rate(1 hour)"
        )
        aws_client.update_event_rule(name=eb_rule, rate=1, period="hour")
        return

    if not listening_now and (current_rule_schedule != "rate(5 minutes)"):
        logger.info(
            "Rescheduling Execution",
            current=current_rule_schedule,
            new="rate(5 minutes)",
        )
        aws_client.update_event_rule(name=eb_rule, rate=5, period="minutes")
        return

    if listening_now and (current_rule_schedule == "rate(5 minutes)"):
        logger.info(
            "Rescheduling Execution",
            current=current_rule_schedule,
            new="rate(1 minute)",
        )
        aws_client.update_event_rule(name=eb_rule, rate=1, period="minute")
        return

    logger.info("Continuing at Existing Schedule", current=current_rule_schedule)


def run(_, context):
    """
    The lambda handler called on function execution

    _:
        the event received on function execution
    context:
        the lambda function metadata
    """
    log_execution(context.function_name, LambdaAction.TRIGGERED)
    aws_client = AWS()
    sp_client = SpotifyClient(aws_client=aws_client)

    try:
        current_song = sp_client.get_current_song()
        reschedule(aws_client=aws_client, listening_now=(current_song is not None))
    except ClientError as ex:
        log_failure(context.function_name, ex)

    log_execution(context.function_name, LambdaAction.COMPLETED)
