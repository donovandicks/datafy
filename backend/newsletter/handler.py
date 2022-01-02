"""Main Lambda function"""

from os import environ

from aws import SES, Dynamo
from aws.models.lambda_func import LambdaAction
from libs.newsletter import Newsletter
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
    logger.info(
        f"Function {LambdaAction.TRIGGERED.name}", function=context.function_name
    )

    newsletter = Newsletter(
        dynamo_client=Dynamo(table_names=environ["SPOTIFY_TABLES"].split(",")),
        ses_client=SES(),
    )
    newsletter.send_report(recipients=[environ["DATAFY_NEWSLETTER_EMAIL"]])

    logger.info(
        f"Function {LambdaAction.COMPLETED.name}", function=context.function_name
    )
