import requests

# Base URL of your API
BASE_URL = "http://127.0.0.1:5000/"

# District ID you want to retrieve
district_id = "d1"

# Make a GET request to the district endpoint
response = requests.get(BASE_URL + f"district/{district_id}")

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON data
    district_data = response.json()
    # Handle the retrieved district data
    print("District data:", district_data)
else:
    # Handle the case when the district was not found or other errors
    print("Failed to retrieve district. Status code:", response.status_code)
