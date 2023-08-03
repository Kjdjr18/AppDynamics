import requests
import xml.etree.ElementTree as ET
#import pandas as pd
#import time
import certifi
import os
#from postman_template import create_postman_json

os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# Replace with your AppDynamics controller info and API token
CONTROLLER_HOST = "controller host"
CONTROLLER_PORT = 443
API_TOKEN = "api token here"
ACCOUNT_NAME = "account name here"
CLIENT_ID = "client ID"
APPLICATION_ID = "app ID"  # Replace with your application ID
TIER_ID="Tier ID here"
DURATION_MIN = 0 # Duration in min
RULE_ID = "HR ID HERE" # replace with your health rule ID
sec = 3 # adjust delay between requests here

#
def get_health_rules():
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/alerting/rest/v1/applications/{APPLICATION_ID}/health-rules"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers, verify=certifi.where())

        if response.status_code == 200:
            root = ET.fromstring(response.text)
            return root
        else:
            print(f"Failed to fetch health rules. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")
        return None


def delete_health_rule(RULE_ID):
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/alerting/rest/v1/applications/{APPLICATION_ID}/health-rules/{RULE_ID}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    try:
        response = requests.delete(url, headers=headers, verify=certifi.where())

        if response.status_code == 200:
            print(f"Successfully deleted health rule with id {RULE_ID}")
        else:
            print(f"Failed to delete health rule. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")



if __name__ == "__main__":
