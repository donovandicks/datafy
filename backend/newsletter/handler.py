"""Main Lambda function"""

from aws.models.lambda_func import LambdaAction
from telemetry.logging import logger


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
    logger.info(f"Function {LambdaAction.TRIGGERED}", function=context.function_name)

    # 1. Scan table for data <= 1 week ago
    # 2. Total play counts
    # 3. Cache play counts (Only need to do step 1 again if cache is lost)
    # 4. Scan table for data > 1 week ago
    # 5. Total play counts
    # 6. Calculate difference in counts (5 - 2)
    # 7. Update cached play count
    # 8. Report to user

    logger.info(f"Function {LambdaAction.COMPLETED}", function=context.function_name)
