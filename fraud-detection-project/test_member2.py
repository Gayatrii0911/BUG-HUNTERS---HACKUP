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
    try:
        response = requests.post(f"{BASE_URL}/transaction", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"Action: {result['action']}")
            print(f"Risk Score: {result['risk_score']}")
            print(f"Anomaly Score: {result['anomaly_score']}")
            print(f"Reasons: {result['reasons']}")
            print(f"Risk Components: {result['risk_components']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    # Test 1: Normal transaction
    test_transaction("user_123", 100.0)
    
    # Test 2: High amount (Anomaly check)
    test_transaction("user_123", 9999.0)
    
    # Test 3: New device/location (Behavior/Device intelligence check)
    test_transaction("user_123", 150.0, device_id="stolen_phone", location="Unknown")

    # Test 4: Critical Fraud (VPN + Impossible Travel + High Amount)
    print("\n--- Testing CRITICAL FRAUD (Should BLOCK) ---")
    payload_fraud = {
        "sender_id": "user_123",
        "receiver_id": "fraudster_xyz",
        "amount": 50000.0,
        "device_id": "device_1", # reuse device_1 but with new location
        "location": "North Korea",
        "channel": "tor"
    }
    response = requests.post(f"{BASE_URL}/transaction", json=payload_fraud)
    result = response.json()
    print(f"Action: {result['action']}")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Reasons: {result['reasons']}")
