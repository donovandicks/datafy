"""Data models for representing the operations of the program
"""

from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel  # pylint: disable=no-name-in-module

T = TypeVar("T")  # pylint: disable=invalid-name


class Status(Enum):
    """An enumeration with values representing the overall status of some task

    Members
    -------
    COMPLETED: 'completed'
    FAILED: 'failed'
    NOT_APPLICABLE: 'not applicable'
    NO_CONTENT: 'no content'
    """

    COMPLETED = "completed"
    """a task reached a valid end-state without errors"""
    FAILED = "failed"
    """an error was encountered during task execution"""
    NOT_APPLICABLE = "not applicable"
    """task execution was not required for the state """
    NO_CONTENT = "no content"
    """task execution received no content """
    NONE = "none"
    """execution was not started, can be used from blank initialization"""


class Task(BaseModel, Generic[T]):
    """Data structure for modeling the outcome of a particular task's execution.

    Any function can return a `Task`. A `Task` should always include a status and either
    an `error` or `data` or both. To include data in the structure, it will have to
    be parameterized with the type of the included data. Any error must inherit from the
    base Python Exception class.

    Example
    -------
    ```python
    def divide(x: int, y: int) -> Task[int]:
        try:
            data = x / y
            return Task(status=Status.COMPLETED, name="divide_ints", data=data)
        except Exception as ex:
            return Task(status=Status.FAILED, name="divide_ints", error=ex)
    ```

    Or with more context:
    ```python
    def divide(x: int, y: int) -> Task[Dict[str, int]]:
        data = {
            'x': x,
            'y': y,
        }
        try:
            data['result'] = x / y
            return Task(status=Status.COMPLETED, name="divide_ints", data=data)
        except Exception as ex:
            return Task(status=Status.FAILED, name="divide_ints", error=ex, data=data)
    ```
    """

    status: Status
    """represents the outcome of the task"""
    name: str
    """the name of the task executed"""
    error: Optional[Exception] = None
    """any error encountered during task execution"""
    data: Optional[T] = None
    """any data returned by the task"""

    class Config:
        """Pydantic config to allow unvalidated types as members"""

        arbitrary_types_allowed = True

    def __str__(self) -> str:
        """Formats the task as a string"""
        # always include the status
        base = f"status:{self.status.value}"

        if not self.error:
            return f"{base} data: {self.data}"

        with_error = f"{base} error: {self.error}"
        if not self.data:
            # if no data just return base + error
            return with_error

        # return status, error, and data
        return f"{with_error} data: {self.data}"

    @property
    def succeeded(self):
        """Checks whether the task failed or not"""
        return self.status != Status.FAILED

    def with_status(self, status: Status):
        """Updates the status of the task"""
        self.status = status
        return self

    def with_error(self, error: Exception):
        self.error = error
        return self

    def with_data(self, data: T):
        self.data = data
        return self


class PipelineStatus(BaseModel):
    """Represents the outcome of a pipeline with the overall status of the execution
    and a list of all tasks performed during execution.
    """

    status: Status
    operations: List[Task]

    def __str__(self) -> str:
        """Formats the pipeline status as a string"""
        return f"status: {self.status.value} operations: {self.operations}"

    @property
    def errors(self) -> List[Optional[Exception]]:
        """Retrieves all errors encountered during pipeline execution"""
        errs = []
        for opr in self.operations:
            if opr.error:
                errs.append(opr.error)
        return errs

    @property
    def summary(self) -> List[Dict[str, str]]:
        return [{task.name: task.status.value} for task in self.operations]

    def log_status(self, logger: Any):
        """Logs the PipelineStatus object

        Params
        ------
        logger: Any
            any logging client that can accept kwargs
        """
        if self.status != Status.COMPLETED:
            logger.error(
                "Pipeline execution failed",
                status=self.status.value,
                tasks=self.summary,
                errors=self.errors,
            )
        else:
            logger.info(
                "Pipeline execution succeeded",
                status=self.status.value,
                tasks=self.summary,
            )

    def with_status(self, status: Status):
        """Updates the status of the pipeline"""
        self.status = status
        return self
