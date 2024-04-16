import json
import boto3
from decimal import Decimal


dynamodb = boto3.resource('dynamodb')
ddbTable = dynamodb.Table("online-resume_Resumes")


def resume_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
    }

    try:
        # Get a list of all resumes
        ddb_response = ddbTable.scan(Select='ALL_ATTRIBUTES')

        # update the visitor counter:
        response_body = ddb_response['Items'][0]

        next_visitor_ctr = response_body.get('resume').get('visitors') + 1

        update_response = ddbTable.update_item(
            Key={"userid": response_body.get('userid')},
            UpdateExpression="set resume.visitors=:ctr",
            ExpressionAttributeValues={':ctr': Decimal(str(next_visitor_ctr))},
            ReturnValues="UPDATED_NEW"
        )


        # convert the number to a string. Else will get a decimal serialization error
        # when converting to JSON.dfc
        response_body['resume']['visitors'] = str(next_visitor_ctr)
        status_code = 200

    except Exception as err:
        status_code = 400
        response_body = {'Error': str(err)}


    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(response_body)
    }

