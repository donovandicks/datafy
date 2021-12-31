"""Main Lambda function"""

import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(_, context):
    """
    The lambda function entry point

    Params
    ------
    event
        the event that triggered the lambda invocation
    context
        metadata about the lambda function
    """
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
