import boto3
import os

LOCALSTACK_HOSTNAME = os.environ.get("LOCALSTACK_HOSTNAME")
ENDPOINT = f"http://{LOCALSTACK_HOSTNAME}:4566"
DYNAMODB_TABLE = "wikipedia"

table = boto3.resource(
    "dynamodb",
    aws_access_key_id="yyyy",
    aws_secret_access_key="xxxx",
    endpoint_url=ENDPOINT,
).Table(DYNAMODB_TABLE)


class db(object):
    @staticmethod
    def put(project, articles):
        return table.put_item(Item={"project": project, "articles": articles})

    @staticmethod
    def get(project):
        return table.get_item(Key={"project": project}).get("Item")
