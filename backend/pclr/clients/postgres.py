"""Code for connection to Postgresql"""

import os
from typing import Any, Dict, List, Optional, Tuple

from clients.secret_manager import SecretManager
from models.db import FilterExpression, UpdateClause

import prefect
import psycopg2


logger = prefect.logging.get_logger(__name__)


class PostgresClient:
    """The postgresql client"""

    table_props = {
        "play_count": [
            "track_id",
            "last_played_timestamp",
            "total_play_count",
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

    def __init__(self, sm_client: SecretManager) -> None:
        self.__sm_client = sm_client
        self.__conn = self.__init_conn()
        self.cursor = self.__conn.cursor()

    def __get_credentials(self) -> Dict:
        """Retrieves DB credentials"""
        rds_secrets_id = os.environ.get("RDS_SECRETS_ID", "")
        secrets = {}

        response = self.__sm_client.get_secrets(sec_id=rds_secrets_id)
        if not response.value:
            raise Exception(f"Failed to retrieve RDS secrets: {response.error}")

        for sec_name in ["RDS_ENDPOINT", "RDS_USER", "RDS_PASSWORD"]:
            secret_key = os.environ.get(sec_name, "")
            if not secret_key:
                raise KeyError(
                    f"Unable to find secret identifier with name {sec_name} in environment"
                )

            secrets[sec_name] = response.value.get(secret_key, "")

        return secrets

    def __init_conn(self):
        """Initializes the DB connection"""
        secrets = self.__get_credentials()
        return psycopg2.connect(
            user=secrets.get("RDS_USER"),
            password=secrets.get("RDS_PASSWORD"),
            host=secrets.get("RDS_ENDPOINT"),
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
