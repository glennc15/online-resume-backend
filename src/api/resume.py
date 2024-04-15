import json



def resume_handler(event, context):
    status_code = 200

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
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',

        },
        'body': json.dumps(message)
    }