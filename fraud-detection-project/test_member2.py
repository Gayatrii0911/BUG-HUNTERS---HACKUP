import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_transaction(sender_id, amount, device_id="device_1", location="New York"):
    payload = {
        "sender_id": sender_id,
        "receiver_id": "receiver_abc",
        "amount": amount,
        "device_id": device_id,
        "location": location,
        "channel": "web"
    }
    
    print(f"\n--- Testing Transaction for {sender_id} (Amount: {amount}) ---")
    response = requests.post(f"{BASE_URL}/transaction", json=payload)
    if response.status_code == 200:
        result = response.json()
        # Updated keys to match Elite API
        print(f"Decision: {result.get('decision', result.get('action', 'N/A'))}")
        print(f"Risk Score: {result.get('risk_score')}")
        print(f"Anomaly Level: {result.get('anomaly_level')} (Score: {result.get('anomaly_score')})")
        print(f"Confidence: {result.get('confidence', 'N/A')}")
        print(f"Reasons: {result.get('reasons')}")
        print(f"Score Breakdown: {json.dumps(result.get('score_breakdown'), indent=2)}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Test 1: Normal transaction
    test_transaction("user_123", 100.0)
    
    # Test 2: High amount (Anomaly check)
    test_transaction("user_123", 9999.0)
    
    # Test 3: New device/location (Behavior/Device intelligence check)
    test_transaction("user_123", 150.0, device_id="stolen_phone", location="Unknown")

    # Test 4: Critical Fraud
    print("\n--- Testing CRITICAL FRAUD (Should BLOCK) ---")
    payload_fraud = {
        "sender_id": "user_123",
        "receiver_id": "fraudster_xyz",
        "amount": 50000.0,
        "device_id": "device_1",
        "location": "North Korea",
        "channel": "tor",
        "timestamp": str(time.time())
    }
    response = requests.post(f"{BASE_URL}/transaction", json=payload_fraud)
    result = response.json()
    print(f"Decision: {result.get('decision')}")
    print(f"Risk Score: {result.get('risk_score')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Reasons: {result.get('reasons')}")
