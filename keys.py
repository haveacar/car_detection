import json
import boto3
from botocore.exceptions import ClientError


class SecretsManager:
    """
    A class for interacting with AWS Secrets Manager.
    """

    def __init__(self, access_key, secret_key, region_name):
        """
        Initialize the SecretsManager with AWS credentials and region.
        """

        self.client = boto3.session.Session().client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def get_secret(self, secret_name):
        """
        Retrieve a secret value from AWS Secrets Manager.
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            print(f"An error occurred: {e}")
            raise e
