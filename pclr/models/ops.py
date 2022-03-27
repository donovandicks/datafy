from enum import Enum
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")  # pylint: disable=invalid-name


class Status(Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    NOT_APPLICABLE = "not applicable"
    NO_CONTENT = "no content"


class Task(BaseModel, Generic[T]):
    status: Status
    error: Optional[Exception] = None
    data: Optional[T] = None

    @property
    def succeeded(self):
        return self.status != Status.FAILED

    class Config:
        arbitrary_types_allowed = True

    def __str__(self) -> str:
        base = f"status:{self.status.value}"
        if self.error:
            return f"{base} error: {self.error}"

        return f"{base} data: {self.data}"


class PipelineStatus(BaseModel):
    status: Status
    operations: List[Task]

    @property
    def errors(self) -> List[Optional[Exception]]:
        errs = []
        for opr in self.operations:
            if opr.error:
                errs.append(opr.error)
        return errs

    def __str__(self) -> str:
        return f"status: {self.status.value} operations: {self.operations}"
