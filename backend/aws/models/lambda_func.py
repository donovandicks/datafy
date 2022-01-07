"""Metadata definitions for AWS Lambda functions"""

from enum import Enum


class LambdaAction(Enum):
    """
    States representing pieces of the lambda function lifecycle
    """

    TRIGGERED = 1
    COMPLETED = 2
    FAILED = 3
