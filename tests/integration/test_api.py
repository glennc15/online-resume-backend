# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import requests

from tests.helpers import get_json_data


def test_get_resume_data_response(global_config):
    respone = requests.get(f"{global_config.get('APIEndpoint')}/resume")
    assert respone.status_code == 200


def test_get_resume_data(global_config):
    respone = requests.get(f"{global_config.get('APIEndpoint')}/resume")
    resume_data = respone.json().get('resume')

    expected_data = get_json_data()


    ignore_keys = ['visitors']
    for k,v in expected_data.items():
        if k not in ignore_keys:
            assert expected_data.get(k) == resume_data.get(k)

    for k,v in resume_data.items():
        if k not in ignore_keys:
            assert resume_data.get(k) == expected_data.get(k)






