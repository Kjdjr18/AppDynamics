# WORKING SCRIPT TO GET LIST OF ALL APPLICATIONS IN CONTROLLER USING REST API ON SAAS CONTROLLER!
import requests

# Replace with your AppDynamics controller info and API token
CONTROLLER_HOST = "metsilabs-nfr.saas.appdynamics.com"
CONTROLLER_PORT = 443
API_TOKEN = "eyJraWQiOiIwYjE2OTY3My0yM2M0LTQ2NTgtYWMzMy00MWY5MDIzZmYxNjciLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBcHBEeW5hbWljcyIsImF1ZCI6IkFwcERfQVBJcyIsImp0aSI6IjlidnllbjAyLVd6cDVPRkIta1RabVEiLCJzdWIiOiJLZW5kYWxfdGVzdCIsImlkVHlwZSI6IkFQSV9DTElFTlQiLCJpZCI6ImU3MWMyMWYwLTFiZjktNDQ4MC05ZWM1LWQ4MDllNmYzNmYzNCIsImFjY3RJZCI6IjBiMTY5NjczLTIzYzQtNDY1OC1hYzMzLTQxZjkwMjNmZjE2NyIsInRudElkIjoiMGIxNjk2NzMtMjNjNC00NjU4LWFjMzMtNDFmOTAyM2ZmMTY3IiwiYWNjdE5hbWUiOiJtZXRzaWxhYnMtbmZyIiwidGVuYW50TmFtZSI6IiIsImZtbVRudElkIjpudWxsLCJhY2N0UGVybSI6W10sInJvbGVJZHMiOltdLCJpYXQiOjE2OTAyMTc3NDEsIm5iZiI6MTY5MDIxNzYyMSwiZXhwIjoxNjkwMzA0MTQxLCJ0b2tlblR5cGUiOiJBQ0NFU1MifQ.PnCNtjFRZo3nhJOlKsxwzTT7XYs36iPbWsjWNoMoHho"
ACCOUNT_NAME = "metsilabs-nfr"


def get_applications():
    # AppDynamics API endpoint to get a list of all applications
    url = f"https://{CONTROLLER_HOST}:{CONTROLLER_PORT}/controller/rest/applications"

    # API request headers with the API token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    # API request parameters
    params = {
        "output": "JSON"
    }

    try:
        # Send the API request with the API token and skip SSL verification
        response = requests.get(url, headers=headers,
                                params=params, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract the list of applications
            applications = data

            # Return the list of applications
            return applications
        else:
            print(
                f"Failed to fetch applications. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the AppDynamics API: {e}")
        return None


if __name__ == "__main__":
    applications_list = get_applications()
    if applications_list:
        print("List of Applications:")
        for app in applications_list:
            print(f"- {app['name']}")