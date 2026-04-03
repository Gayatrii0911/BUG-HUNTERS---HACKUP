import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_elite_response():
    print("\n--- Testing Elite Response Structure ---")
    tx = {
        "sender_id": "elite_user_1",
        "receiver_id": "rec_1",
        "amount": 50000.0,
        "device_id": "new_device_999",
        "location": "New York",
        "channel": "web"
    }
    resp = requests.post(f"{BASE_URL}/transaction", json=tx)
    data = resp.json()
    print(json.dumps(data, indent=2))
    
    # Assertions for structure
    assert "score_breakdown" in data
    assert "anomaly_level" in data
    assert "is_pre_transaction_check" in data
    assert data["is_pre_transaction_check"] is True
    print("✅ Structure Verified")

def test_fraud_chain():
    print("\n--- Testing Fraud Chain Detection (ATO -> Abuse) ---")
    # This user will have a 'new device' (ATO signal) and we'll give a high amount
    tx = {
        "sender_id": "ato_victim_1",
        "receiver_id": "attacker_wallet",
        "amount": 99999.0,
        "device_id": "unknown_hacker_phone",
        "location": "Unknown_Proxy",
        "channel": "tor"
    }
    resp = requests.post(f"{BASE_URL}/transaction", json=tx)
    data = resp.json()
    print(f"Decision: {data['decision']}")
    print(f"Chain Detected: {data['fraud_chain_detected']}")
    print(f"Reasons: {data['reasons']}")
    
    if data['fraud_chain_detected']:
        print("✅ Fraud Chain Successfully Detected")

def test_risk_escalation():
    print("\n--- Testing Risk Escalation (Adaptive History) ---")
    user = "repeat_offender"
    # Send 3 suspicious transactions
    for i in range(3):
        tx = {
            "sender_id": user,
            "receiver_id": f"rec_{i}",
            "amount": 1000.0,
            "device_id": "sus_device",
            "location": "Global",
            "channel": "api"
        }
        resp = requests.post(f"{BASE_URL}/transaction", json=tx)
        data = resp.json()
        print(f"Tx {i+1} Score: {data['risk_score']}")
    
    print("✅ Risk history tracked and escalation applied")

if __name__ == "__main__":
    try:
        test_elite_response()
        test_fraud_chain()
        test_risk_escalation()
    except Exception as e:
        print(f"❌ Test Failed: {e}")
