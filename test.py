import requests

BASE = "http://127.0.0.1:5000/"

data = [{"district_id": "d40", "name": "Scho"},
        {"district_id": "d20", "name": "Sberg"},
        {"district_id": "d50", "name": "Schberg"}]


#for i in range(len(data)):
    #response = requests.put(BASE + "district/" + str(i), data[i])
    #print(response.json())

response = requests.get(BASE + "district/d40")
print(response.json())