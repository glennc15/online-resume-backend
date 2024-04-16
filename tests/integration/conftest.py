# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import botocore
import boto3

import os
import pytest
import time
import uuid
import json

from tests.helpers import get_dynamodb_json, get_terraform_outputs, get_json_data


globalConfig = {}


def clear_dynamo_tables():
    # clear all data from the tables that will be used for testing
    dbd_client = boto3.client('dynamodb')
    db_response = dbd_client.scan(
        TableName=globalConfig['ResumeTable'],
        AttributesToGet=['userid']
    )
    for item in db_response["Items"]:
        dbd_client.delete_item(
            TableName=globalConfig['ResumeTable'],
            Key={'userid': {'S': item['userid']["S"]}}
        )
    return


def create_resume_record():

    record_data = {
        'userid': str(uuid.uuid1()),
        # 'resume': get_dynamodb_json()
        'resume': get_json_data()

    }

    dbd_client = boto3.resource('dynamodb')
    ddb_table = dbd_client.Table(globalConfig.get("ResumeTable"))
    create_result = ddb_table.put_item(
        Item=record_data
    )

    return create_result


@pytest.fixture(scope='session')
def global_config(request):
    global globalConfig
    globalConfig.update(get_terraform_outputs())
    clear_dynamo_tables()
    globalConfig.update(create_resume_record())

    yield globalConfig

    clear_dynamo_tables()
    create_resume_record()