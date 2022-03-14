from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")  # pylint: disable=invalid-name


@dataclass
class Result(Generic[T]):
    """Models an object that either has a value or an error related to the
    intended value.
    """

    value: Optional[T]
    error: Optional[str]
