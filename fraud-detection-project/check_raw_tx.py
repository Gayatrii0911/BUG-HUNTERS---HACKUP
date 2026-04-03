import http.client
import json

conn = http.client.HTTPConnection("localhost", 8000)
headers = {'Content-Type': 'application/json'}
payload = json.dumps({
    "sender_id": "Test_User_01",
    "receiver_id": "Recipient_X",
    "amount": 7500.0,
    "location": "Mumbai",
    "device_id": "DEV_ALPHA"
})
conn.request("POST", "/transaction", payload, headers)
r = conn.getresponse()
print(r.read().decode())
conn.close()
