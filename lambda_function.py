from src.main import main
import json


def lambda_handler(event, context):
    try:
        status_code, body = main(**event)
    except Exception as e:
        status_code, body = 500, {'message': 'Internal server error: ' + str(e)}

    return {
        'headers': {'content-type': 'application/json; charset=utf-8'},
        'statusCode': status_code,
        'body': json.dumps(body)
    }