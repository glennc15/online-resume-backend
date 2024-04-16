import json
import boto3

from tests.helpers import get_terraform_outputs

print("get_terraform_outputs()")
print(get_terraform_outputs())

dynamodb = boto3.resource('dynamodb')
ddbTable = dynamodb.Table(USERS_TABLE)


def resume_handler(event, context):
    status_code = 400
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
    }

    body = {
        'message': "Hello World!",
        'event': event,
    }

    # results = {
    #     "statusCode": status_code,
    #     "headers": headers,
    #     "body": body,
    # }

    # return json.dumps(results)


    message = {
    'message': 'Execution started successfully!',
    'event': event,
    }



    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(message)
    }

    # return {
    #     'statusCode': 200,
    #     'headers': {
    #         'Content-Type': 'application/json',

    #     },
    #     'body': json.dumps(message)
    # }