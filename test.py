import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "district/1", {"district_id": "d10", "name": "Schoneberg"})
print(response.json())