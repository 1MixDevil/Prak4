import requests
name = input()
check = {
    "name": name,
    "room": 1
}

resp = requests.post("http://127.0.0.1:5000/connect", json=check)