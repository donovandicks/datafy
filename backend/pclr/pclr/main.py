# pyright: reportPrivateImportUsage=false
from datetime import datetime, timedelta

import prefect
from prefect import task, Flow
from prefect.schedules import IntervalSchedule


schedule = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1),
    interval=timedelta(seconds=5),
)


@task
def get_ten():
    """Returns 10"""
    return 10


@task
def ping_out():
    """Logs message"""
    logger = prefect.context.get("logger")
    logger.info("Pinging from prefect!")


with Flow("Test-Docker", schedule=schedule) as flow:
    ping_out()

if __name__ == "__main__":
    flow.run()
