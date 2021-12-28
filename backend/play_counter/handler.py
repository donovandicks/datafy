"""Main entry point for the play-counter lambda"""

from structlog import get_logger

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

    try:
        sp_client = SpotifyClient()
        sp_client.get_current_song()
    except Exception as ex:
        logger.log_failure(context.function_name, ex)

    logger.log_execution(context.function_name, LambdaAction.COMPLETED)
