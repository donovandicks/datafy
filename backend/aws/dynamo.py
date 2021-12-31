"""Code for working with DynamoDB"""

from os import environ
from typing import Optional

from boto3 import resource
from boto3.dynamodb.conditions import ComparisonCondition
from botocore.exceptions import ClientError
from telemetry.logging import logger


class Dynamo:
    """Wrapper for AWS DynamoDB"""

    def __init__(self, table_names: list[str]) -> None:
        self.__table_names = table_names
        self.__client = resource(
            "dynamodb",
            region_name=environ["REGION_NAME"],
        )
        self.dynamo_tables = self.__init_tables()

    def __init_tables(self) -> dict:
        tables = {}
        for name in self.__table_names:
            logger.info("Initializing DynamoDB Table", table_name=name)
            tables[name.strip()] = self.__client.Table(name.strip())

        return tables

    def __get_table(self, table_name: str):
        if table_name not in self.dynamo_tables:
            raise KeyError(f"Table {table_name} is not valid")

        return self.dynamo_tables[table_name]

    def get_item(
        self, table_name: str, key_name: str, key_val: str, attributes: list[str]
    ) -> dict:
        """
        Retrieves an item from the dynamo table

        Params
        ------
        key_name: str
            the name of the primary key in the dynamo table
        key_val: str
            the value of the primary key to match on
        attributes: list[str]
            the list of attributes to retrieve from the table item

        Returns
        -------
        an object containing the item retrieved from dynamo

        Raises
        ------
        a botocore `ClientError` if an error occurs while retrieving an item
        """
        try:
            return self.__get_table(table_name=table_name).get_item(
                Key={key_name: key_val},
                ProjectionExpression=", ".join(attributes),
            )
        except ClientError as ex:
            logger.error(
                "Failed to retrieve an item from Dynamo",
                key_name=key_name,
                key_value=key_val,
            )
            raise ex

    def insert_item(self, table_name: str, item: dict) -> dict:
        """
        Inserts an item into the dynamo table

        Params
        ------
        item: dict
            an object of key-value pairs representing a new item to be inserted
            into the dynamo table

        Returns
        -------
        an object containing the item inserted into dynamo

        Raises
        ------
        a botocore `ClientError` if an error occurs while inserting an item
        """
        try:
            return self.__get_table(table_name=table_name).put_item(
                Item=item,
                ReturnValues="ALL_OLD",
            )
        except ClientError as ex:
            logger.error("Failed to insert item into Dynamo table", item=item)
            raise ex

    def update_item(
        self,
        table_name: str,
        key_name: str,
        key_val: str,
        update_expr: str,
        expr_vals: dict,
    ) -> dict:
        """
        Updates an existing item in the dynamo table

        Params
        ------
        key_name: str
            the name of the primary key in the dynamo table
        key_val: str
            the value of the primary key to match on
        update_expr: str
            an expression used to update specific keys on the dynamo item
        expr_vals: dict
            a mapping that identifies the new values for the keys being updated

        Returns
        -------
        an object containing the item inserted into dynamo

        Raises
        ------
        a botocore `ClientError` if an error occurs while inserting an item
        """
        try:
            return self.__get_table(table_name=table_name).update_item(
                Key={key_name: key_val},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_vals,
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as ex:
            logger.error(
                "Failed to update item",
                key_name=key_name,
                key_value=key_val,
            )
            raise ex

    def scan_table(
        self,
        table_name: str,
        filter_expr: Optional[ComparisonCondition] = None,
    ) -> list[dict]:
        """
        Scans a table
        """
        table = self.__get_table(table_name=table_name)
        items = []

        if filter_expr:
            logger.info(
                "Scanning Table With Filter",
                table_name=table_name,
                filter=filter_expr.get_expression(),
            )

            items = table.scan(
                FilterExpression=filter_expr,
            ).get("Items", [{}])
        else:
            logger.info("Scanning Table", table_name=table_name)
            items = table.scan().get("Items", [{}])

        logger.info("Retrieved Items", item_count=len(items))
        return items
