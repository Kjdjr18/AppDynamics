import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
import os

# Replace with your AppDynamics controller info and API token
CONTROLLER_HOST = ""    # controller host domain 
CONTROLLER_PORT = 443   # Controller Port, Default 443
API_TOKEN = ""          # Api Token  
ACCOUNT_NAME = ""       # controller account name
APPLICATION_NAME = ""   # Replace with your application name or ID
DURATION_MIN = "43200"  # 1 month


def get_metric_data(metric_path):
    # AppDynamics API endpoint to get metric data
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/rest/applications/{APPLICATION_NAME}/metric-data"

    # API request headers with the API token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # API request parameters
    params = {
        "metric-path": metric_path,
        "time-range-type": "BEFORE_NOW",
        "duration-in-mins": DURATION_MIN
    }

    try:
        # Send the GET request with the API token
        response = requests.get(url, headers=headers, params=params, verify=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.text)

            # Get the sum of the metric values
            sum = int(root.find('.//sum').text)

            return sum
        else:
            print(f"Failed to fetch metric data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")
        return None


def get_business_transactions_data():
    # AppDynamics API endpoint to get business transactions data
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/rest/applications/{APPLICATION_NAME}/business-transactions"

    # API request headers with the API token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # API request parameters
    params = {
        "time-range-type": "BEFORE_NOW",
        "duration-in-mins": DURATION_MIN
    }

    try:
        # Send the GET request with the API token
        response = requests.get(url, headers=headers, params=params, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.text)

            # Create a list of dictionaries, each containing the data of a business transaction
            data = []
            for bt in root.findall('business-transaction'):
                bt_name = bt.find('name').text
                tier_name = bt.find('tierName').text

                # Get the total calls for this business transaction
                total_calls = get_metric_data(
                    f"Business Transaction Performance|Business Transactions|{tier_name}|{bt_name}|Calls per Minute")

                data.append({
                    'id': bt.find('id').text,
                    'name': bt_name,
                    'app': APPLICATION_NAME,
                    'tier': tier_name,
                    'entryPointType': bt.find('entryPointType').text,
                    'Total Calls': total_calls
                })

            # Convert the list of dictionaries to a pandas Data Frame
            df = pd.DataFrame(data)

            # Save the DataFrame to a CSV file
            results_folder = os.path.expanduser("~/Desktop/appd_api_results")
            os.makedirs(results_folder, exist_ok=True)
            df.to_csv(os.path.join(results_folder, 'business_transactions.csv'), index=False)

            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(os.path.join(results_folder, 'business_transactions.csv'))

            # Write the DataFrame to an Excel file
            df.to_excel(os.path.join(results_folder, 'business_transactions.xlsx'), index=False)
            print(f"Saved {len(df)} business transactions to business_transactions.csv")
        else:
            print(f"Failed to fetch business transactions data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")

    # Wait for 5 seconds
    time.sleep(5)

    # Get the total number of calls and errors
    total_calls = get_metric_data("Overall Application Performance|Calls per Minute")
    total_errors = get_metric_data("Overall Application Performance|Errors per Minute")

    # Calculate the error rate
    if total_calls is not None and total_errors is not None:
        error_rate = (total_errors / total_calls) * 100
        error_rate = round(error_rate)
        print(f"Error rate: {error_rate}%")

        # Create a DataFrame with the results
        df = pd.DataFrame({
            'Total Calls': [total_calls],
            'Total Errors': [total_errors],
            'Error Rate (%)': [error_rate]
        })

        # Save the DataFrame to a CSV file
        df.to_csv(os.path.join(results_folder, 'error_rate.csv'), index=False)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(results_folder, 'error_rate.csv'))

        # Write the DataFrame to an Excel file
        df.to_excel(os.path.join(results_folder, 'error_rate.xlsx'), index=False)
        print(f"Saved error rate to error_rate.csv")


if __name__ == "__main__":
    get_business_transactions_data()
