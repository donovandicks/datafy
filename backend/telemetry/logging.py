"""Code for logging"""

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
