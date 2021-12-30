"""Code for interacting with AWS"""

from json import loads
from os import environ

from boto3 import client, resource, session
from botocore.exceptions import ClientError
from telemetry.logging import Logger

logger = Logger(module_name=__name__)


def parse_sm_error(err_obj: ClientError, sec_name: str) -> str:
    """
    Parses a secret manager error into a useful log string

    Params
    ------
    err_obj: ClientError
        the original error object
    sec_name: str
        the name of the secret that was being retrieved
    """
    err_code = err_obj.response["Error"]["Code"]
    err_msgs = {
        "ResourceNotFoundException": f"The secret {sec_name} was not found",
        "InvalidRequestException": f"The secret request was invalid: {err_obj}",
        "DecryptionFailure": f"The secret cannot be decrypted: {err_obj}",
        "InternalServiceErrorException": f"An error occurred on AWS server side: {err_obj}",
    }

    if err_code in err_msgs:
        return err_msgs[err_code]

    return f"An unexpected error occurred retrieving secret {sec_name}: {err_obj}"


class AWS:
    """The AWS Client Wrapper"""

    def __init__(self) -> None:
        self.__boto3_session = session.Session()
        self.__dynamo_client = resource(
            "dynamodb",
            region_name=environ["REGION_NAME"],
        )
        self.eb_client = client("events")

        self.dynamo_tables = {
            environ["SPOTIFY_TRACKS_TABLE"]: self.__dynamo_client.Table(
                environ["SPOTIFY_TRACKS_TABLE"]
            ),
            environ["SPOTIFY_CACHE_TABLE"]: self.__dynamo_client.Table(
                environ["SPOTIFY_CACHE_TABLE"]
            ),
        }
        self.sm_client = self.__boto3_session.client(
            service_name="secretsmanager",
            region_name=environ["REGION_NAME"],
        )

    def __get_table(self, table_name: str):
        if table_name not in self.dynamo_tables:
            raise KeyError(f"Table {table_name} is not valid")

        return self.dynamo_tables[table_name]

    def get_secret(self, sec_name: str) -> str:
        """
        Retrieves a secret from AWS secret manager

        Params
        ------
        sec_name: str
            the name of the secret in AWS SM

        Returns
        _______
        secret: str
            the secret retrieved from AWS
        """
        try:
            secrets = self.sm_client.get_secret_value(
                SecretId=environ["SPOTIFY_SECRETS"]
            ).get("SecretString")
            return loads(secrets)[sec_name]

        except ClientError as ex:
            logger.error(
                "Failed to retrieve secret", error=parse_sm_error(ex, sec_name)
            )
            raise ex

    def get_dynamo_item(
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

    def insert_dynamo_item(self, table_name: str, item: dict) -> dict:
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

    def update_dynamo_item(
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

    def get_event_rule(self, name: str) -> dict:
        """
        Retrieves details about an EventBridge rule

        Params
        ------
        name: str
            the name of the rule to retrieve

        Returns
        -------
        an object containing information about the EventBridge rule

        Raises
        ------
        `ClientError` if an error is encountered when retrieving the rule from AWS
        """
        logger.info("Retrieving EventBridge Rule", name=name)
        try:
            rule = self.eb_client.describe_rule(Name=name)
            return rule
        except ClientError as ex:
            logger.error(
                "Failed to retrieve EventBridge Rule", name=name, error=str(ex)
            )
            raise ex

    def get_rule_schedule(self, name: str) -> str:
        """
        Retrieves the schedule for the rule with the given name

        Params
        ------
        name: str
            the name of the EventBridge rule to retrieve the schedule for

        Returns
        -------
        the schedule expression of the rule
        """
        logger.info("Retrieving EventBridge Rule Schedule", name=name)
        return self.get_event_rule(name=name).get("ScheduleExpression", "")

    def update_event_rule(self, name: str, rate: int, period: str):
        """
        Updates an EventBridge rule

        Params
        ------
        rate: int
            the number of `period`s to pass before triggering the event again
        period: str
            the time period to pass (minute, hour, etc.)
        """
        assert rate >= 1

        logger.info("Updating EventBridge Rule", name=name, rate=rate)
        expression = f"rate({rate} {period})"
        self.eb_client.put_rule(
            Name=name,
            ScheduleExpression=expression,
        )
