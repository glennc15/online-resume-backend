# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import os
import boto3
import uuid
import pytest
from moto import mock_dynamodb
from contextlib import contextmanager
from unittest.mock import patch

from tests.helpers import get_json_data, get_dynamodb_json, get_terraform_outputs


print("get_terraform_outputs()")
print(get_terraform_outputs())

USERS_MOCK_TABLE_NAME = get_terraform_outputs().get("ResumeTable")
UUID_MOCK_VALUE_JOHN = 'f8216640-91a2-11eb-8ab9-57aa454facef'
UUID_MOCK_VALUE_JANE = '31a9f940-917b-11eb-9054-67837e2c40b0'
UUID_MOCK_VALUE_NEW_USER = 'new-user-guid'


def mock_uuid():
    return UUID_MOCK_VALUE_NEW_USER


@contextmanager
def my_test_environment():
    with mock_dynamodb():
        set_up_dynamodb()
        put_data_dynamodb()
        yield

def set_up_dynamodb():
    conn = boto3.client(
        'dynamodb'
    )
    conn.create_table(
        TableName=USERS_MOCK_TABLE_NAME,
        KeySchema=[
            {'AttributeName': 'userid', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'userid', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

def put_data_dynamodb():
    conn = boto3.client(
        'dynamodb'
    )




    resume = get_dynamodb_json()
    # resume = get_json_data()

    print(f"USERS_MOCK_TABLE_NAME = {USERS_MOCK_TABLE_NAME}")
    print(f"resume = {resume}")

    conn.put_item(
            TableName=USERS_MOCK_TABLE_NAME,
            Item={
                'userid': {'S': UUID_MOCK_VALUE_JOHN},
                'resume': {'M': resume},
            }
        )


@patch.dict(os.environ, {'USERS_TABLE': USERS_MOCK_TABLE_NAME, 'AWS_XRAY_CONTEXT_MISSING': 'LOG_ERROR'})
def test_get_resume():
    with my_test_environment():
        from src.api import resume
        with open('./events/event-get-resume.json', 'r') as f:
            apigw_get_all_users_event = json.load(f)

        expected_response = get_json_data()
        expected_response['visitors'] = '638'

        ret = resume.resume_handler(apigw_get_all_users_event, '')
        assert ret['statusCode'] == 200

        data = json.loads(ret['body']).get('resume')

        # assert data == expected_response

        for k,v in expected_response.items():
            assert expected_response.get(k) == data.get(k)


def test_get_resume_visitor_counter():
    with my_test_environment():
        from src.api import resume
        with open('./events/event-get-resume.json', 'r') as f:
            apigw_get_all_users_event = json.load(f)


        expected_response = get_json_data()
        expected_visitor_ctr = expected_response.get('visitors')

        # calls the lambda function several times and checks the visitor counter
        # properly updated in the database:
        for idx in range(6):
            expected_visitor_ctr += 1
            expected_response['visitors'] = str(expected_visitor_ctr)

            # call the lambda function:
            ret = resume.resume_handler(apigw_get_all_users_event, '')

            assert ret['statusCode'] == 200

            data = json.loads(ret['body']).get('resume')

            for k,v in expected_response.items():
                assert expected_response.get(k) == data.get(k)



