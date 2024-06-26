import requests
import json

# Base URL of your API
BASE_URL = "http://127.0.0.1:5000/"

# Helper function to print responses
def print_response(response):
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except json.JSONDecodeError:
        print("Response Text:", response.text)

# Test GET request for a district
def test_get_district(district_id):
    response = requests.get(BASE_URL + f"district/{district_id}")
    print("GET District:")
    print_response(response)

# Test PUT request for a district
def test_put_district(district_id, put_data):
    response = requests.put(BASE_URL + f"district/{district_id}", json=put_data)
    print("PUT District:")
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

# Test PATCH request for a district
def test_patch_district(district_id, updates):
    response = requests.patch(BASE_URL + f"district/{district_id}", json=updates)
    print("PATCH District:")
    print_response(response)

# Test DELETE request for a district
def test_delete_district(district_id,):
    response = requests.delete(BASE_URL + f"district/{district_id}")
    print("DELETE District:")
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

# Example data for testing
district_id = "d1"
put_data = {
    "district_id": district_id,
    "dist_name": "New District Name",
    "stores": [
        {
            "store_id": "s1",
            "store_name": "Store 1",
            "address": "Address 1",
            "products": [
                {
                    "item": "Product 1",
                    "price": 10.0
                }
            ]
        }
    ]
}
patch_data = {
    "dist_name": "Updated District Name",
    "stores": json.dumps([
        {
            "store_id": "s1",
            "store_name": "Store 1",
            "address": "Address 1",
            "products": [
                {
                    "item": "Product 1",
                    "price": 10.0
                }
            ]
        }
    ])
}

# Run tests
#print("Running GET test:")
#test_get_district(district_id)

print("\nRunning PUT test:")
test_put_district(district_id, put_data)

#print("\nRunning PATCH test:")
#test_patch_district(district_id, patch_data)

#print("\nRunning DELETE test:")
#test_delete_district(district_id)


