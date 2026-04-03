from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def make_tx(sender, receiver, amount, device="device_1", location="NY"):
    return {
        "sender_id": sender,
        "receiver_id": receiver,
        "amount": amount,
        "device_id": device,
        "location": location
    }

def print_result(name, res):
    print(f"--- {name} ---")
    data = res.json()
    print("Action:", data.get("action"))
    print("Risk Score:", data.get("risk_score"))
    print("Reasons:", data.get("reasons"))
    print("Graph flags:", {
        "cycle": data.get("graph_signals", {}).get("has_cycle"),
        "hub/suspicious": data.get("graph_signals", {}).get("suspicious_connections"),
        "rapid": data.get("graph_signals", {}).get("rapid_transactions")
    })
    print()

def run_tests():
    print("=== STAGE 2: API & GRAPH TESTS ===")
    
    # 1. Normal
    client.post("/debug/reset", json={}) # assuming a reset endpoint exists or just rely on a clean state
    
    r = client.post("/transaction", json=make_tx("AccountA", "AccountB", 100))
    print_result("Test 1: Normal", r)

    # 2. Chain
    client.post("/transaction", json=make_tx("AccountB", "AccountC", 100))
    client.post("/transaction", json=make_tx("AccountC", "AccountD", 100))
    r = client.post("/transaction", json=make_tx("AccountD", "AccountE", 100))
    print_result("Test 2: Suspicious Chain", r)

    # 3. Cycle
    r = client.post("/transaction", json=make_tx("AccountE", "AccountA", 100))
    print_result("Test 3: Cycle", r)

    # 4. Hub
    for char in ["F", "G", "H", "I", "J"]:
        r = client.post("/transaction", json=make_tx("AccountA", f"Account{char}", 50))
    print_result("Test 4: Hub / High Connections", r)

    print("=== STAGE 4: MEMBER 1 + 2 ML INTEGRATION ===")
    # 5. Anomalous ML + Graph
    # Sending huge amount from new device + impossible travel
    r = client.post("/transaction", json=make_tx("AccountA", "AccountZ", 50000, "evil_device", "RUSSIA"))
    print_result("Test 5: Anomaly + Graph High Risk", r)

    print("=== STAGE 3: TRACE API ===")
    t = client.get("/trace/AccountA")
    if t.status_code == 200:
        print("Trace API works. Data length:", len(str(t.json())))
    else:
        print("Trace API issue or endpoint missing")

if __name__ == "__main__":
    run_tests()
