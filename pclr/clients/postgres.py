"""Code for connection to Postgresql"""

import os
from typing import Any, List, Type, TypeAlias

from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

Table: TypeAlias = Type[SQLModel]


class PostgresClient:
    """The postgresql client"""

    def __init__(self) -> None:
        self.__debug = bool(os.getenv("DATAFY_DEBUG", ""))
        self.__engine = create_engine(
            url="postgresql://localhost:5432/datafy", echo=self.__debug
        )

    def insert(self, item: SQLModel) -> None:
        """Inserts a record into the database"""
        with Session(self.__engine) as session:
            session.add(item)
            session.commit()

    def update(
        self,
        table: Table,
        filter_key: str,
        filter_value: Any,
        update_key: str,
        update_value: Any,
    ):
        """Updates a record where the filter_key equals the filter_value"""
        with Session(self.__engine) as session:
            stmt = select(table).where(filter_key == filter_value)
            result: SQLModel = session.exec(stmt).one()

            setattr(result, update_key, update_value)
            session.add(result)
            session.commit()

    def get_all_rows(self, table: Table) -> List:
        """Retrieves all rows from a table"""
        with Session(self.__engine) as session:
            return session.exec(select(table)).all()

    def get_row(self, table: Table, key: str, value: Any) -> List:
        """Retrieves a single row where the conditions are met"""
        with Session(self.__engine) as session:
            stmt = select(table).where(key == value)
            return session.exec(stmt).all()

    def check_exists(self, table: Table, key: str, value: Any) -> bool:
        """Checks if a row exists on a table where the given key matches the value"""
        return bool(self.get_row(table=table, key=key, value=value))
