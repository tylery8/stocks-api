import boto3
from decimal import Decimal


class Client:

    def __init__(self, cls, table, partition_key):
        self.cls = cls
        self.table = boto3.resource('dynamodb').Table(table)
        self.partition_key = partition_key

    def get_item(self, key):
        response = self.table.get_item(Key={self.partition_key: key})
        return self.cls(**Client.from_dynamo(response['Item'])) if 'Item' in response else None

    def put_item(self, item):
        return self.table.put_item(Item=self.to_dynamo(item.__dict__))

    def delete_item(self, key):
        return self.table.delete_item(Key={self.partition_key: key})

    def index(self, attribute):
        response = self.table.scan(ProjectionExpression=attribute)
        return [item[attribute] for item in response['Items']]

    @staticmethod
    def to_dynamo(obj):
        if isinstance(obj, list):
            return list(Client.to_dynamo(el) for el in obj)
        elif isinstance(obj, dict):
            return {f'numeric_key_{k}' if isinstance(k, int) else k: Client.to_dynamo(v)
                    for k, v in obj.items()}
        elif isinstance(obj, set):
            return set(Client.to_dynamo(el) for el in obj)
        elif isinstance(obj, float):
            return Decimal(str(obj))
        else:
            return obj

    @staticmethod
    def from_dynamo(dynamo_obj):
        if isinstance(dynamo_obj, list):
            return list(Client.from_dynamo(el) for el in dynamo_obj)
        elif isinstance(dynamo_obj, dict):
            return {int(k[12:]) if k.startswith('numeric_key_') else k: Client.from_dynamo(v)
                    for k, v in dynamo_obj.items()}
        elif isinstance(dynamo_obj, set):
            return set(Client.from_dynamo(el) for el in dynamo_obj)
        elif isinstance(dynamo_obj, Decimal):
            return int(dynamo_obj) if dynamo_obj % 1 == 0 else float(dynamo_obj)
        else:
            return dynamo_obj
