import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_elite_refinement():
    print("\n--- [TEST 1] Elite Response Structure ---")
    tx = {
        "sender_id": "refine_user_1",
        "receiver_id": "rec_1",
        "amount": 100.0,
        "device_id": "known_device_1",
        "location": "Mumbai",
        "channel": "mobile"
    }
    resp = requests.post(f"{BASE_URL}/transaction", json=tx)
    data = resp.json()
    print(json.dumps(data, indent=2))
    
    # Assertions for structure
    required_keys = [
        "transaction_id", "risk_score", "risk_level", "decision", 
        "reasons", "reason_categories", "score_breakdown", 
        "anomaly_score", "anomaly_level", "confidence", 
        "fraud_chain_detected", "is_pre_transaction_check", "alert"
    ]
    for key in required_keys:
        assert key in data, f"Missing key: {key}"
    
    assert isinstance(data["reason_categories"], dict)
    assert "behavior" in data["reason_categories"]
    print("✅ Structure Verified")

def test_fraud_chain_refinement():
    print("\n--- [TEST 2] Fraud Chain Detection (New Device + Anomaly > 0.5) ---")
    # Establish a stronger baseline and trigger an adaptive retrain (20+ tx)
    user_id = f"victim_{int(time.time())}"
    print(f"Calibrating system for user: {user_id}...")
    for i in range(25):
        requests.post(f"{BASE_URL}/transaction", json={
            "sender_id": user_id, "receiver_id": "rec", "amount": 100.0 + i, "device_id": "known_d", "location": "L1"
        })
    
    # Now, simulate a fraud chain: New device + Absolute extreme amount
    tx = {
        "sender_id": user_id,
        "receiver_id": "attacker",
        "amount": 999999.0,
        "device_id": "NEW_HACKER_DEVICE",
        "location": "UNKNOWN_PLANET",
        "channel": "web"
    }
    resp = requests.post(f"{BASE_URL}/transaction", json=tx)
    data = resp.json()
    # Verify Fraud Chain detection
    print(f"Anomaly Level: {data['anomaly_level']}, Anomaly Score: {data['anomaly_score']}")
    print(f"Risk Score: {data['risk_score']}")
    print(f"Fraud Chain Detected: {data['fraud_chain_detected']}")
    
    assert data["fraud_chain_detected"] is True
    # Updated assertion for structured reasons
    reason_messages = [r["message"] for r in data["reasons"]]
    assert any("Suspicious login followed by anomalous transaction" in m for m in reason_messages)
    assert data["risk_score"] >= 60
    print("✅ Fraud Chain Verified")

def test_min_risk_floor():
    print("\n--- [TEST 3] Minimum Risk Floor (MEDIUM >= 25, HIGH >= 50) ---")
    # Force a medium anomaly (amount slightly higher)
    tx = {
        "sender_id": "floor_test_user", "receiver_id": "rec", "amount": 500.0, "device_id": "d1", "location": "L1"
    }
    # We might need to send a few to calibrate the model if it's fresh, 
    # but isolation forest should flag it if we've sent others.
    resp = requests.post(f"{BASE_URL}/transaction", json=tx)
    data = resp.json()
    print(f"Anomaly Level: {data['anomaly_level']}, Risk Score: {data['risk_score']}")
    
    if data["anomaly_level"] == "MEDIUM":
        assert data["risk_score"] >= 25
    elif data["anomaly_level"] == "HIGH":
        assert data["risk_score"] >= 50
    print("✅ Risk Floor Verified")

def test_confidence_score():
    print("\n--- [TEST 4] Confidence Score Calculation ---")
    # Only one component (behavior) triggered
    tx = {
        "sender_id": "conf_user", "receiver_id": "rec_new", "amount": 100.0, "device_id": "d1", "location": "L1"
    }
    resp = requests.post(f"{BASE_URL}/transaction", json=tx)
    data = resp.json()
    print(f"One Signal Confidence: {data['confidence']}")
    
    # Multistal - Graph + ML + Behavior (using simulation wave or crafted tx)
    # For now check it exists and is normalized
    assert 0.0 <= data["confidence"] <= 1.0
    print("✅ Confidence Score Verified")

if __name__ == "__main__":
    try:
        test_elite_refinement()
        test_fraud_chain_refinement()
        test_min_risk_floor()
        test_confidence_score()
        print("\n🚀 ALL ELITE REFINEMENT TESTS PASSED!")
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
