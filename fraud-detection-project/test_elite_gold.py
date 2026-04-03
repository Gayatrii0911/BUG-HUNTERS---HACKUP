import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_simulation(scenario):
    print(f"\n--- Triggering {scenario.upper()} simulation ---")
    try:
        response = requests.post(f"{BASE_URL}/simulation/run/{scenario}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['scenario']} completed with {result['steps']} steps.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    # 1. Run a normal wave to populate DB and trigger retraining eventually
    test_simulation("normal_user")
    
    # 2. Check health
    time.sleep(1)
    print("\n--- Verifying server status ---")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        print(f"Health Response: {resp.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # 3. Run an ATO attack simulation
    test_simulation("account_takeover")
    
    # 4. Run a Fraud Ring (Cycle) simulation
    test_simulation("cycle_fraud")
    
    # 5. Run Synthetic Identity (Coordinated) simulation
    test_simulation("coordinated_synergy")
    
    print("\nElite Gold Verification Complete. Check uvicorn terminal for '[ML] Retraining' logs.")
