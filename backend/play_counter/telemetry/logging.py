"""Code for logging"""

from models.lambda_state import LambdaAction
from structlog import configure
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import BoundLogger, add_log_level, get_logger

configure(
    wrapper_class=BoundLogger,
    processors=[
        add_log_level,
        TimeStamper(fmt="iso"),
        JSONRenderer(
            sort_keys=True,
        ),
    ],
)

logger = get_logger()


def log_execution(func_name: str, action: LambdaAction):
    """
    Logs a key moment in lambda execution

    func_name: str
        the name of the lambda function
    action: FunctionAction
        the lambda lifecycle event to log for
    """
    logger.info(f"Function {action.name}", function_name=func_name)


def log_failure(func_name: str, exception: Exception):
    """
    Logs the failure of a lambda function
    """
    logger.error(
        f"Function {LambdaAction.FAILED.name} due to exception",
        function_name=func_name,
        exception=str(exception),
    )
