import requests

URL = "http://127.0.0.1:5000/mfa"

for i in range(5):
    data = {"token": "000000"}
    r = requests.post(URL, data=data)
    print("Attempt", i + 1, r.text)
