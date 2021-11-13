"""Defines the abstract base class for adapter classes"""

from abc import ABC, abstractmethod
from typing import Any


class Adapter(ABC):
    """The base adapter pattern"""

    def __init__(self, data: dict) -> None:
        super().__init__()
        self.data = data

    @abstractmethod
    def make_table(self) -> list[list[Any]]:
        """
        Format data as a table - eg:
        ```
        [
            [a, b, c],
            [1, 2, 3]
        ]
        ```
        """
