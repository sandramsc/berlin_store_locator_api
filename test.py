import requests

BASE = "http://127.0.0.1:5000/"

data = [{"district_id": "d88", "dist_name": "Milkll"},
    {"district_id": "d89", "dist_name": "sssilkll"},
]


for i in range(len(data)):
    response = requests.get(BASE + "district/d88" + str(i), data[i])

#print(response.json())

#response = requests.get(BASE + "district/d88")
#print(response.json())