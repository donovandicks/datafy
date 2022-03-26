"""Code for connection to Postgresql"""

import os
from typing import Any, List, Optional, Tuple

import psycopg2
from models.db import FilterExpression, UpdateClause


class PostgresClient:
    """The postgresql client"""

    table_props = {
        "play_count": [
            "track_id",
            "last_played_timestamp",
            "total_play_count",
            "popularity",
        ],
        "track": [
            "track_id",
            "track_name",
            "artist_id",
            "album_id",
        ],
        "artist": [
            "artist_id",
            "artist_name",
        ],
        "album": [
            "album_id",
            "album_name",
        ],
    }

    def __init__(self) -> None:
        self.__conn = self.__init_conn()
        self.cursor = self.__conn.cursor()

    def __init_conn(self):
        """Initializes the DB connection"""
        return psycopg2.connect(
            user=os.environ.get("POSTGRES_USER", ""),
            password=os.environ.get("POSTGRES_PASSWORD", ""),
            host="localhost",
            port=5432,
            database="datafy",
            connect_timeout=3,
        )

    def __close_cursor(self) -> None:
        """Closes an open cursor"""
        if self.cursor:
            self.cursor.close()

    def __validate_table(self, table_name: str) -> None:
        if not table_name in self.table_props:
            raise KeyError(f"Invalid table name: {table_name}")

    def __run_query(
        self,
        query: str,
        params: Optional[Tuple] = None,
        keep_alive: Optional[bool] = False,
    ) -> None:
        """Executes a query"""
        if self.cursor.closed:
            self.cursor = self.__conn.cursor()
        self.cursor.execute(query=query, vars=params)

        self.__conn.commit()

        if not keep_alive and not self.cursor.closed:
            self.__close_cursor()

    def insert(self, table: str, values: Tuple) -> None:
        """Inserts a record into the database"""
        self.__validate_table(table)

        sql = f"""
        INSERT INTO {table}
        ({','.join(self.table_props[table])})
        VALUES ({','.join(["%s" for _ in self.table_props[table]])});
        """
        self.__run_query(query=sql, params=values)

    def update(self, table: str, clause: UpdateClause):
        """Updates a record where the filter_key equals the filter_value

        class UpdateClause {
            update_field: str
            new_value: str
            filter_field: str
            filter_condition: str,
            filter_value: Any
        }
        """
        self.__validate_table(table)

        sql = f"""
        UPDATE {table}
        SET {clause.update_field} = {clause.update_field} + 1
        WHERE {clause.filter_expr.filter_field} {clause.filter_expr.filter_condition} {clause.filter_expr.filter_value!r}
        """
        self.__run_query(query=sql)

    def get_all_rows(self, table: str) -> List[Tuple[Any]]:
        """Retrieves all rows from a table"""
        sql = f"SELECT * FROM {table}"
        self.__run_query(query=sql, keep_alive=True)
        results = self.cursor.fetchall()
        self.__close_cursor()
        return results

    def get_row(self, table: str, filter_expr: FilterExpression) -> Tuple:
        """Retrieves a single row where the conditions are met"""
        sql = f"""
        SELECT *
        FROM {table}
        WHERE {filter_expr.build_filter_expression()}
        """
        self.__run_query(query=sql, keep_alive=True)
        result = self.cursor.fetchone()
        self.__close_cursor()
        return result
