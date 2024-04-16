# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import botocore
import boto3

import os
import pytest
import time
import uuid
import json

from tests.helpers import get_dynamodb_json, get_terraform_outputs


globalConfig = {}

# def get_terraform_outputs():
#     terraform_outputs = subprocess.run(['terraform output'], stdout=subprocess.PIPE, shell=True)
#     terraform_str = terraform_outputs.stdout.decode('utf-8')
#     terraform_parts = [x.split(' = ') for x in terraform_str.split('\n')]
#     terraform_outputs = dict([(x[0], x[1][1:-1]) for x in terraform_parts if len(x) > 1])

#     return terraform_outputs


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
        'resume': get_dynamodb_json()
    }

    # print(record_data)

    dbd_client = boto3.resource('dynamodb')
    ddb_table = dbd_client.Table(globalConfig.get("ResumeTable"))
    create_result = ddb_table.put_item(
        Item=record_data
    )

    return create_result


@pytest.fixture(scope='session')
def global_config(request):
    global globalConfig




    # globalConfig.update({'UsersTable': 'tf-serverless-patterns_Users'})
    # globalConfig.update({"status": "Hi"})
    # load outputs of the stacks to test
    # globalConfig.update(get_stack_outputs(APPLICATION_STACK_NAME))
    # globalConfig.update(create_cognito_accounts())

    terraform_outputs = get_terraform_outputs()
    # terraform_outputs['ResumeTable'] = terraform_outputs.get('resume_table')

    globalConfig.update(terraform_outputs)
    print(globalConfig)

    clear_dynamo_tables()
    globalConfig.update(create_resume_record())

    return globalConfig
