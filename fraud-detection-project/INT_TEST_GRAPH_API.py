import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api_integration():
    print("=== STARTING API INTEGRATION TEST (GRAPH FLOW) ===")
    
    # 1. Reset Simulation
    print("Resetting system...")
    requests.post(f"{BASE_URL}/simulation/reset")
    
    # 2. Submit a transaction that creates a cycle (A -> B -> C -> A)
    txs = [
        {"sender_id": "USER_A", "receiver_id": "USER_B", "amount": 100, "device_id": "dev1"},
        {"sender_id": "USER_B", "receiver_id": "USER_C", "amount": 100, "device_id": "dev1"},
        {"sender_id": "USER_C", "receiver_id": "USER_A", "amount": 100, "device_id": "dev1"}
    ]
    
    for i, tx in enumerate(txs):
        print(f"Submitting TX {i+1}: {tx['sender_id']} -> {tx['receiver_id']}")
        resp = requests.post(f"{BASE_URL}/transaction", json=tx)
        if resp.status_code != 200:
            print(f"  [ERROR] Status {resp.status_code}: {resp.text}")
            continue
            
        data = resp.json()
        
        # Check if score_breakdown exists
        if "score_breakdown" in data:
            breakdown = data["score_breakdown"]
            graph_risk = breakdown.get("graph_risk", 0)
            print(f"  Risk: {data.get('risk_score')} (Graph: {graph_risk})")
            if i == 2: # The cycle should be detected on the 3rd TX
                if graph_risk >= 30: # Cycle gives significant risk
                    print("  [PASS] Cycle detected (increased graph risk)!")
                else:
                    print(f"  [FAIL] Cycle NOT reflected in graph risk ({graph_risk}).")
        else:
            print("  [ERROR] No score_breakdown in response")

    # 3. Test Trace API
    print("\nTesting Trace API for USER_A...")
    resp = requests.get(f"{BASE_URL}/trace/USER_A")
    data = resp.json()
    if data["status"] == "success":
        print(f"  [PASS] Trace API responsive. Found {data['path_count']} paths.")
        print(f"  Max Path Length: {data['max_path_length']}")
        if data.get("graph_payload"):
             print(f"  [PASS] Graph payload included (Nodes: {len(data['graph_payload']['nodes'])})")
    else:
        print("  [FAIL] Trace API failed")

    print("\n=== API INTEGRATION TEST COMPLETE ===")

if __name__ == "__main__":
    try:
        test_api_integration()
    except Exception as e:
        print(f"FAILED: {e}")
