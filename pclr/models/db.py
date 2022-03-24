from dataclasses import dataclass
from typing import Any


@dataclass
class FilterExpression:
    """A model for a SQL filter expression

    Returns:
        _type_: _description_
    """

    filter_field: str

    filter_condition: str

    filter_value: Any

    def build_filter_expression(self) -> str:
        """Converts the filter values to a an expression"""
        return f"{self.filter_field} {self.filter_condition} '{self.filter_value}'"


@dataclass
class UpdateClause:
    """A model for a SQL update clause

    Returns:
        _type_: _description_
    """

    update_field: str

    update_value: str

    filter_expr: FilterExpression

    def build_set_expression(self) -> str:
        return f"{self.update_field} = {self.update_value}"
