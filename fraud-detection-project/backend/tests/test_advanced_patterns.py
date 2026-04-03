from fastapi.testclient import TestClient
from backend.main import app
import time

client = TestClient(app)

def make_tx(sender, receiver, amount, device="device_1", location="NY"):
    # Use real-time timestamps for velocity checks
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
    print(f"CASE: {name}")
    if res.status_code != 200:
        print("Error:", res.status_code, res.text); return
    data = res.json()
    print("DECISION:", data.get("decision"))
    print("RISK_SCORE:", data.get("risk_score"), f"({data.get('risk_level')})")
    print("REASONS:", data.get("reasons"))
    print("-" * 30)

def run_tests():
    print("=== ELITE PATTERN VALIDATION ===\n")
    client.post("/debug/reset")
    
    # 1. Smurfing Pattern (3 quick transactions between same accounts)
    print("Simulating Smurfing pattern...")
    client.post("/transaction", json=make_tx("SmurfA", "SmurfB", 100))
    client.post("/transaction", json=make_tx("SmurfA", "SmurfB", 100))
    r = client.post("/transaction", json=make_tx("SmurfA", "SmurfB", 100))
    print_result("Structuring / Smurfing", r)

    # 2. Velocity Layering (A -> B -> C rapidly)
    print("Simulating Velocity Layering...")
    client.post("/debug/reset")
    client.post("/transaction", json=make_tx("LayerA", "LayerB", 100))
    r = client.post("/transaction", json=make_tx("LayerB", "LayerC", 100))
    print_result("High Velocity Layering", r)

    # 3. Synthetic Identity (3 users on ONE device)
    print("Simulating Synthetic Identity...")
    client.post("/debug/reset")
    client.post("/transaction", json=make_tx("User1", "Merchant", 100, device="HARDWARE_X"))
    client.post("/transaction", json=make_tx("User2", "Merchant", 100, device="HARDWARE_X"))
    r = client.post("/transaction", json=make_tx("User3", "Merchant", 100, device="HARDWARE_X"))
    print_result("Synthetic Identity (Shared Device)", r)

    # 4. Dense Cluster (Clique)
    print("Simulating Fraud Cluster...")
    client.post("/debug/reset")
    client.post("/transaction", json=make_tx("NodeA", "NodeB", 100))
    client.post("/transaction", json=make_tx("NodeB", "NodeC", 100))
    client.post("/transaction", json=make_tx("NodeC", "NodeA", 100))
    r = client.post("/transaction", json=make_tx("NodeA", "NodeC", 100))
    print_result("Dense Fraud Cluster", r)

if __name__ == "__main__":
    run_tests()
