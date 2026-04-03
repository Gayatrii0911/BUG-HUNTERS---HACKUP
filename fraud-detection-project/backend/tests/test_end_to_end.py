from fastapi.testclient import TestClient
from backend.main import app
import time

client = TestClient(app)

def make_tx(sender, receiver, amount, device="device_1", location="NY"):
    return {
        "sender_id": sender,
        "receiver_id": receiver,
        "amount": amount,
        "device_id": device,
        "location": location,
        "channel": "mobile",
        "timestamp": str(time.time())
    }

def print_result(name, res):
    print(f"==============================")
    print(f"CASE: {name}")
    print(f"==============================")
    if res.status_code != 200:
        print("Error:", res.status_code, res.text)
        return
        
    data = res.json()
    print("FINAL_DECISION:", data.get("decision"))
    print("FINAL_RISK_SCORE:", data.get("risk_score"), f"({data.get('risk_level')})")
    print("ANOMALY_LEVEL:", data.get("anomaly_level"))
    print("FRAUD_CHAIN_DETECTED:", data.get("fraud_chain_detected"))
    print("EXPLANATION_REASONS:", data.get("reasons"))
    print("BREAKDOWN_GRAPH:", data.get("score_breakdown", {}).get("graph_risk"))
    print("BREAKDOWN_ML:", data.get("score_breakdown", {}).get("ml_risk"))
    print("BREAKDOWN_BEHAVIOR:", data.get("score_breakdown", {}).get("behavior_risk"))
    print("BREAKDOWN_DEVICE:", data.get("score_breakdown", {}).get("device_risk"))
    print(f"==============================\n")

def run_tests():
    print("STARTING ELITE VALIDATION...\n")
    client.post("/debug/reset")
    
    # Test 1: Normal
    r = client.post("/transaction", json=make_tx("AccountA", "AccountB", 100))
    print_result("Test 1: Normal", r)
    time.sleep(0.5)

    # Test 2: Anomaly
    r = client.post("/transaction", json=make_tx("AccountA", "AccountZ", 5000, "evil_device", "MOSCOW"))
    print_result("Test 2: Anomaly", r)
    time.sleep(0.5)

    # Test 3: Cycle
    client.post("/debug/reset")
    client.post("/transaction", json=make_tx("X", "Y", 100))
    client.post("/transaction", json=make_tx("Y", "Z", 100))
    r = client.post("/transaction", json=make_tx("Z", "X", 100))
    print_result("Test 3: Cycle Detection", r)
    time.sleep(0.5)

    # Test 4: Coordinated Fraud
    client.post("/debug/reset")
    client.post("/transaction", json=make_tx("M1", "M2", 100))
    client.post("/transaction", json=make_tx("M2", "M3", 100))
    r = client.post("/transaction", json=make_tx("M3", "M1", 80000, "scam_device", "RUSSIA"))
    print_result("Test 4: Coordinated Fraud Boost", r)

if __name__ == "__main__":
    run_tests()
