import http.client
import json

def test_sentinel():
    conn = http.client.HTTPConnection("localhost", 8000)
    
    print("\n--- [1] TESTING SCORING ---")
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
    body = r.read().decode()
    res = json.loads(body)
    print("Full Response Keys:", list(res.keys()))
    print("Full Response:", body)

    print("\n--- [2] TESTING HEALTH ---")
    conn.request("GET", "/health")
    r2 = conn.getresponse()
    body2 = r2.read().decode()
    res2 = json.loads(body2)
    print("Full Health Keys:", list(res2.keys()))
    print("Full Health Response:", body2)
    
    conn.close()

if __name__ == "__main__":
    test_sentinel()
