"""Code for logging"""
from datetime import datetime

from models.lambda_state import LambdaAction


def get_current_time() -> str:
    """
    Returns the current time as "HH:MM:SS.MILLI"
    """
    return str(datetime.now().time())


class Logger:
    """Logging Wrapper"""

    def __init__(self, logger):
        self.logger = logger

    def info(self, *args, **kwargs):
        """Wrapper for the logger's own `info` method"""
        self.logger.info(*args, **kwargs)

    def warn(self, *args, **kwargs):
        """Wrapper for the logger's own `warn` method"""
        self.logger.warn(*args, **kwargs)

    def error(self, *args, **kwargs):
        """Wrapper for the logger's own `error` method"""
        self.logger.error(*args, **kwargs)

    def debug(self, *args, **kwargs):
        """Wrapper for the logger's own `debug` method"""
        self.logger.debug(*args, **kwargs)

    def log_execution(self, func_name: str, action: LambdaAction):
        """
        Logs a key moment in lambda execution

        func_name: str
            the name of the lambda function
        action: FunctionAction
            the lambda lifecycle event to log for
        """
        self.logger.info(
            f"Function {action.name}", function_name=func_name, time=get_current_time()
        )

    def log_failure(self, func_name: str, exception: Exception):
        """
        Logs the failure of a lambda function
        """
        self.logger.error(
            f"Function {LambdaAction.FAILED.name} due to exception",
            function_name=func_name,
            time=get_current_time,
            exception=exception,
        )
