import http.client
import json

def test_sentinel():
    conn = http.client.HTTPConnection("localhost", 8000)
    
    print("\n--- [1] TESTING REAL-TIME SCORING ---")
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({
        "sender_id": "Test_User_01",
        "receiver_id": "Recipient_X",
        "amount": 7500.0,
        "location": "Mumbai",
        "device_id": "DEV_ALPHA"
    })
    try:
        conn.request("POST", "/transaction", payload, headers)
        r = conn.getresponse()
        res = json.loads(r.read().decode())
        print(f"Decision: {res['decision']} | Risk Score: {res['risk_score']}")
        print(f"Confidence: {res['confidence']} | Anomaly Level: {res['anomaly_level']}")
    except Exception as e:
        print(f"Error in Scoring API: {e}")

    print("\n--- [2] TESTING ALERTS FEED ---")
    try:
        conn.request("GET", "/alerts")
        r = conn.getresponse()
        data = json.loads(r.read().decode())
        alerts = data.get("alerts", [])
        print(f"Active Alerts in Stream: {len(alerts)}")
    except Exception as e:
        print(f"Error in Alerts API: {e}")

    print("\n--- [3] TESTING GRAPH TRACE ---")
    try:
        conn.request("GET", "/trace/Test_User_01")
        r = conn.getresponse()
        res = json.loads(r.read().decode())
        print(f"Graph Status: {res['status']} | Nodal Reach: {res['path_count']}")
        print(f"Graph Payload Nodes: {len(res['graph_payload']['nodes'])}")
    except Exception as e:
        print(f"Error in Trace API: {e}")

    print("\n--- [4] TESTING NEURAL MONITOR ---")
    try:
        conn.request("GET", "/health")
        r = conn.getresponse()
        res = json.loads(r.read().decode())
        print(f"Engine Status: {res['status']}")
        print(f"Adaptive Loop Progress: {res['adaptive_learning']['progress_percent']}%")
    except Exception as e:
        print(f"Error in Health API: {e}")

    conn.close()

if __name__ == "__main__":
    test_sentinel()
