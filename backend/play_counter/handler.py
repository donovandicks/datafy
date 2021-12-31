"""Main entry point for the play-counter lambda"""
from datetime import datetime, time
from os import environ

from botocore.exceptions import ClientError

from aws import Dynamo, EventBridge, SecretManager
from aws.models.lambda_func import LambdaAction
from clients.spotify import SpotifyClient
from telemetry.logging import logger


def reschedule(eb_client: EventBridge, listening_now: bool):
    """
    Reschedules the EventBridge rule responsible for triggering this lambda

    Params
    ------
    aws_client: AWS
    listening_now: bool
    """
    eb_rule = environ["EVENT_BRIDGE_RULE"]
    current_rule_schedule = eb_client.get_rule_schedule(name=eb_rule)

    if (
        time.fromisoformat("02:00:00")
        < datetime.now().time()
        < time.fromisoformat("08:00:00")
    ) and (current_rule_schedule != "rate(1 hour)"):
        logger.info(
            "Rescheduling Execution", current=current_rule_schedule, new="rate(1 hour)"
        )
        eb_client.update_event_rule(name=eb_rule, rate=1, period="hour")
        return

    if not listening_now and (current_rule_schedule != "rate(5 minutes)"):
        logger.info(
            "Rescheduling Execution",
            current=current_rule_schedule,
            new="rate(5 minutes)",
        )
        eb_client.update_event_rule(name=eb_rule, rate=5, period="minutes")
        return

    if listening_now and (current_rule_schedule == "rate(5 minutes)"):
        logger.info(
            "Rescheduling Execution",
            current=current_rule_schedule,
            new="rate(1 minute)",
        )
        eb_client.update_event_rule(name=eb_rule, rate=1, period="minute")
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
    logger.info(f"Function {LambdaAction.TRIGGERED}", function=context.function_name)
    sp_client = SpotifyClient(dynamo_client=Dynamo(), secret_manager=SecretManager())

    try:
        current_song = sp_client.get_current_song()
        reschedule(eb_client=EventBridge(), listening_now=(current_song is not None))
    except ClientError as ex:
        logger.exception(
            f"Function {LambdaAction.FAILED}", funcion=context.function_name, error=ex
        )

    logger.info(f"Function {LambdaAction.COMPLETED}", function=context.function_name)
