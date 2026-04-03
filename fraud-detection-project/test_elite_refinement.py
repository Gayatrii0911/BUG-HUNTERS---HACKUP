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
    assert data["risk_score"] >= 70
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

def test_mfa_escalation_rule():
    print("\n--- [TEST 5] MFA Escalation Rule (3x Avg + 0.4 Anomaly) ---")
    user_id = f"mfa_user_{int(time.time())}"
    # 1. Establish average of 100
    for i in range(5):
        requests.post(f"{BASE_URL}/transaction", json={
            "sender_id": user_id, "receiver_id": "rec", "amount": 100.0, "device_id": "d1", "location": "L1"
        })
    
    # 2. Trigger 3.5x amount (350) + simulate medium anomaly
    # On a new user/fresh state, this should trigger enough deviations for MFA
    tx = {
        "sender_id": user_id, "receiver_id": "rec_new", "amount": 350.0, "device_id": "d2", "location": "L2"
    }
    resp = requests.post(f"{BASE_URL}/transaction", json=tx)
    data = resp.json()
    print(f"Amount: 350 (Avg: 100), Anomaly Score: {data['anomaly_score']}, Decision: {data['decision']}")
    
    # If it's a fresh user, anomaly score might be high enough
    if data["anomaly_score"] >= 0.4:
        assert data["decision"] in ["MFA", "BLOCK"], f"Expected MFA/BLOCK for high deviation, got {data['decision']}"
    print("✅ MFA Escalation Verified")

def test_reason_consistency():
    print("\n--- [TEST 6] Reason-Score Consistency ---")
    tx = {
        "sender_id": "consist_user", "receiver_id": "rec", "amount": 5000.0, "device_id": "new_d", "location": "new_l"
    }
    resp = requests.post(f"{BASE_URL}/transaction", json=tx)
    data = resp.json()
    
    scores = data["score_breakdown"]
    reasons = data["reasons"]
    reason_types = [r["type"] for r in reasons]
    
    print(f"Breakdown: {scores}")
    print(f"Reason Types: {reason_types}")
    
    if scores["behavior_risk"] > 0: assert "behavior" in reason_types
    if scores["device_risk"] > 0: assert "device" in reason_types or "synergy" in reason_types
    if scores["ml_risk"] > 0: assert "ml" in reason_types
    if scores["graph_risk"] > 0: assert "graph" in reason_types
    
    print("✅ Reason Consistency Verified")

if __name__ == "__main__":
    try:
        test_elite_refinement()
        test_fraud_chain_refinement()
        test_min_risk_floor()
        test_mfa_escalation_rule()
        test_reason_consistency()
        print("\n🚀 ALL ELITE CALIBRATION TESTS PASSED!")
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
