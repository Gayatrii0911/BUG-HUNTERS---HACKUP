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
    res = json.loads(r.read().decode())
    print("Full Response Keys:", res.keys())
    if 'confidence' in res:
        print(f"Confidence: {res['confidence']}")

    print("\n--- [2] TESTING HEALTH ---")
    conn.request("GET", "/health")
    r = conn.getresponse()
    res = json.loads(r.read().decode())
    print("Full Health Keys:", res.keys())
    if 'adaptive_learning' in res:
        print("Adaptive Learning exists.")
    else:
        print("Adaptive Learning MISSING!")
    
    conn.close()

if __name__ == "__main__":
    test_sentinel()
