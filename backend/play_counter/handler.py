"""Main entry point for the play-counter lambda"""

import datetime
import logging

from clients.spotify import Client

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def log_start(func_name: str):
    """
    Logs the execution of a lambda function

    func_name: str
        the name of the lambda function
    """
    current_time = datetime.datetime.now().time()
    logger.info("Function %s ran at %s", func_name, str(current_time))


def run(_, context):
    """
    The lambda handler called on function execution

    _:
        the event received on function execution
    context:
        the lambda function metadata
    """
    log_start(context.function_name)
    sp_client = Client()
    sp_client.get_current_song()
