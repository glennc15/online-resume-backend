# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import requests

from tests.helpers import get_dynamodb_json


def test_get_resume_data_response(global_config):
    respone = requests.get(f"{global_config.get('APIEndpoint')}/resume")
    assert respone.status_code == 200

def test_get_resume_data(global_config):
    respone = requests.get(f"{global_config.get('APIEndpoint')}/resume")
    resume_data = respone.json()
    print(respone.json())


    expected_data = get_dynamodb_json()

    for k,v in expected_data.items():
        assert expected_data.get(k) == resume_data.get(k)

    for k,v in resume_data.items():
        assert resume_data.get(k) == expected_data.get(k)






# tf-serverless-patterns_rest_api

# def test_access_to_the_users_without_authentication(global_config):
#     response = requests.get(global_config["APIEndpoint"] + '/users')
#     assert response.status_code == 401

# def test_get_list_of_users_by_regular_user(global_config):
#     response = requests.get(
#         global_config["APIEndpoint"] + '/users',
#         headers={'Authorization': global_config["regularUserIdToken"]}
#     )
#     assert response.status_code == 403

# def test_deny_post_user_by_regular_user(global_config):
#     response = requests.post(
#         global_config["APIEndpoint"] + '/users',
#         data=json.dumps(new_user),
#         headers={'Authorization': global_config["regularUserIdToken"],
#                  'Content-Type': 'application/json'}
#     )
#     assert response.status_code == 403

# def test_allow_post_user_by_administrative_user(global_config):
#     response = requests.post(
#         global_config["APIEndpoint"] + '/users',
#         data=json.dumps(new_user),
#         headers={'Authorization': global_config["adminUserIdToken"],
#                  'Content-Type': 'application/json'}
#     )
#     assert response.status_code == 200
#     data = json.loads(response.text)
#     assert data['name'] == new_user['name']
#     global new_user_id
#     new_user_id = data['userid']

# def test_deny_post_invalid_user(global_config):
#     new_invalid_user = {"Name": "John Doe"}
#     response = requests.post(
#         global_config["APIEndpoint"] + '/users',
#         data=new_invalid_user,
#         headers={'Authorization': global_config["adminUserIdToken"],
#                  'Content-Type': 'application/json'}
#     )
#     assert response.status_code == 400

# def test_get_user_by_regular_user(global_config):
#     response = requests.get(
#         global_config["APIEndpoint"] + f'/users/{new_user_id}',
#         headers={'Authorization': global_config["regularUserIdToken"]}
#     )
#     assert response.status_code == 403
