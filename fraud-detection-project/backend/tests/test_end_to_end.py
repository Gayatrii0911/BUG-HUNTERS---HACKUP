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
    print(f"--- {name} ---")
    data = res.json()
    print("Action:", data.get("action"))
    print("Risk Score:", data.get("risk_score"))
    print("Reasons:", data.get("reasons"))
    
    # Verify graph contract
    signals = data.get("graph_signals", {})
    print("Graph flags:", {
        "cycle": signals.get("has_cycle"),
        "hub/chain": signals.get("suspicious_connections"),
        "rapid": signals.get("rapid_transactions"),
        "m1_score": signals.get("score")
    })
    print()

def run_tests():
    print("=== M1 + M2 UNIFIED VALIDATION ===")
    
    # Reset
    print("Resetting system state...")
    client.post("/debug/reset")
    
    # 1. Normal
    # This should be Low risk
    r = client.post("/transaction", json=make_tx("A", "B", 100))
    print_result("Test 1: Normal", r)

    # 2. Chain (Member 1 logic)
    # A -> B -> C -> D -> E
    client.post("/transaction", json=make_tx("B", "C", 100))
    client.post("/transaction", json=make_tx("C", "D", 100))
    r = client.post("/transaction", json=make_tx("D", "E", 100))
    print_result("Test 2: Suspicious Chain (4+ Hops)", r)

    # 3. Cycle (Member 1 logic)
    # E -> A (closes cycle)
    r = client.post("/transaction", json=make_tx("E", "A", 100))
    print_result("Test 3: Cycle Detection (A->B->C->D->E->A)", r)

    # 4. Anomaly (Member 2 logic)
    # New device, unknown location, huge amount
    r = client.post("/transaction", json=make_tx("A", "X", 10000, "scam_device", "NORTH_POLE"))
    print_result("Test 4: Behavioral Anomaly Only", r)

    # 5. Combined Fraud (Elite Tier)
    # Hub behavior + Anomaly
    for char in ["F", "G", "H", "I"]:
        client.post("/transaction", json=make_tx("A", f"User{char}", 50))
    
    r = client.post("/transaction", json=make_tx("A", "UserJ", 50, "new_device", "LA"))
    print_result("Test 5: Hub Account + Behavioral Deviation", r)

    print("\n=== TRACE API VERIFICATION ===")
    t = client.get("/trace/A")
    print("Status:", t.status_code)
    if t.status_code == 200:
        print("Trace Response contains paths:", "paths" in t.json())
        print("Trace Response contains graph_payload:", "graph_payload" in t.json())
    
    print("\n=== ALERTS VERIFICATION ===")
    a = client.get("/alerts")
    print("Blocked Alerts found:", len(a.json().get("alerts", [])))

if __name__ == "__main__":
    run_tests()
