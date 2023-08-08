import requests
import certifi
import os

#WARNING, THIS SCRIPT CAN DELETE ALL POLICIES, HEALTH RULES AND ACTIONS.

os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

CONTROLLER_HOST = "account-name.saas.appdynamics.com" # prepend .saas.appdynamics.com with your account name
CONTROLLER_PORT = 443
API_TOKEN = "API-TOKEN"  #add API Token generated here
ACCOUNT_NAME = "account-name"  #add your account name here
CLIENT_ID = "client-id@account-name" #replace with your client ID @ account name
APPLICATION_ID = "12345"  #Add your application ID

WHITE_LIST_POLICIES = ["", ""]
WHITE_LIST_ACTIONS = ["", ""]
WHITE_LIST_HEALTH_RULES = ["12345", "23456", "34567", "45678", "56789"]


def get_entities(endpoint):
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/alerting/rest/v1/applications/{APPLICATION_ID}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers, verify=certifi.where())
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch {endpoint}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")
        return None


def delete_entity(endpoint, entity_id):
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/alerting/rest/v1/applications/{APPLICATION_ID}/{endpoint}/{entity_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    try:
        response = requests.delete(url, headers=headers, verify=certifi.where())
        if response.status_code == 200 or response.status_code == 204:
            print(f"Successfully deleted {endpoint} with id {entity_id}")
        else:
            print(f"Failed to delete {endpoint}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")


def process_entities(endpoint, whitelist):
    entities = get_entities(endpoint)
    delete_list = []
    preserve_list = []

    if entities:
        for entity in entities:
            entity_id = str(entity['id'])
            if entity_id not in whitelist:
                delete_list.append(entity_id)
            else:
                preserve_list.append(entity_id)

    print(f"IDs to be deleted from {endpoint}: {delete_list}")
    print(f"IDs to be preserved in {endpoint}: {preserve_list}")

    delete_confirmation = input("Do you want to delete the listed items? (y/n): ")
    if delete_confirmation.lower() == 'y':
        for entity_id in delete_list:
            delete_entity(endpoint, entity_id)
    elif delete_confirmation.lower() == 'n':
        print(f"List of IDs preserved for {endpoint}: {preserve_list}")
    else:
        print("Invalid input. No action taken.")


process_entities('policies', WHITE_LIST_POLICIES)
process_entities('actions', WHITE_LIST_ACTIONS)
process_entities('health-rules', WHITE_LIST_HEALTH_RULES)
