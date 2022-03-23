import uuid
import structlog
from structlog import configure
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import BoundLogger, add_log_level, get_logger

configure(
    wrapper_class=BoundLogger,
    processors=[
        structlog.threadlocal.merge_threadlocal,
        add_log_level,
        TimeStamper(fmt="iso"),
        JSONRenderer(sort_keys=False),
    ],
)

logger = get_logger()


def bind_pipeline():
    structlog.threadlocal.clear_threadlocal()
    structlog.threadlocal.bind_threadlocal(
        execution_id=str(uuid.uuid4()),
    )
