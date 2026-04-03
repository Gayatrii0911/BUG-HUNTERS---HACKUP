import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def log_result(test_name, success, info=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} | {test_name.ljust(30)} | {info}")

def run_stress_test():
    requests.post(f"{BASE_URL}/debug/reset")

    # 1. MVP: Normal Flow
    r = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "user1", "receiver_id": "user2", "amount": 50.0, "location": "Mumbai"
    }).json()
    log_result("MVP: Normal Flow", r['decision'] == "APPROVE", f"Score: {r['risk_score']}")

    # 2. MVP: Cold Start (THE ONE THAT FAILED)
    r = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "new_user_cold", "receiver_id": "user2", "amount": 100.0, "location": "L1", "device_id": "D1"
    }).json()
    print(f"DEBUG Cold Start Response: {json.dumps(r, indent=2)}")
    log_result("MVP: Cold Start", r['decision'] in ["APPROVE", "MFA"], f"Decision: {r['decision']}, Score: {r['risk_score']}")

    # 3. Synergy
    for i in range(11): 
        requests.post(f"{BASE_URL}/transaction", json={"sender_id": "BOSS", "receiver_id": f"M_{i}", "amount": 5})
    r = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "BOSS", "receiver_id": "M_0", "amount": 99999.0, "location": "XYZ", "device_id": "EVIL_HW"
    }).json()
    log_result("Advanced: Synergy", r['risk_score'] >= 70, f"Score: {r['risk_score']}")

if __name__ == "__main__":
    run_stress_test()
