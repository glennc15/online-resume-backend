import json
import subprocess

def get_dynamodb_json():
    with open("./tests/unit/expected_data_dynamodb.json", "r") as f:
    # with open("./tests/unit/expected_data.json", "r") as f:

        dynamodb_json = json.loads(f.read())

    return dynamodb_json


def get_terraform_outputs():
    terraform_outputs = subprocess.run(['cd terraform && terraform output'], stdout=subprocess.PIPE, shell=True)
    terraform_str = terraform_outputs.stdout.decode('utf-8')
    terraform_parts = [x.split(' = ') for x in terraform_str.split('\n')]
    terraform_outputs = dict([(x[0], x[1][1:-1]) for x in terraform_parts if len(x) > 1])

    return terraform_outputs


def get_json_data():
    with open("./tests/unit/expected_data.json", "r") as f:
        json_data = json.loads(f.read())

    return json_data