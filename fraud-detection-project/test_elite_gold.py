import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001"

def test_simulation(pattern, count=5):
    print(f"\n--- Triggering {pattern.upper()} simulation ({count} tx) ---")
    payload = {"pattern": pattern, "count": count}
    try:
        response = requests.post(f"{BASE_URL}/simulate", json=payload)
        if response.status_code == 200:
            print(f"Success: {response.json()['message']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    # 1. Run a normal wave to populate DB and trigger retraining eventually
    # RETRAIN_THRESHOLD is 20, so we run 22 normal ones
    test_simulation("normal", count=22)
    
    # 2. Check health after retraining should have happened
    time.sleep(2)
    print("\n--- Verifying server status after retraining ---")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        print(f"Health Response: {resp.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # 3. Run an ATO attack simulation
    test_simulation("ato", count=1)
    
    # 4. Run a Fraud Ring simulation
    test_simulation("fraud_ring", count=5)
    
    print("\nElite Gold Verification Complete. Check uvicorn terminal for '[ML] Retraining' logs.")
