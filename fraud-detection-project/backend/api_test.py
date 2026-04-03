from fastapi.testclient import TestClient
from backend.main import app
from backend.graph.builder import reset_graph
from datetime import datetime

client = TestClient(app)

def make_tx(from_acc, to_acc, amount):
    return {
        "user_id": "U_" + from_acc,
        "from_account": from_acc,
        "to_account": to_acc,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat(),
        "device_id": "D1",
        "channel": "mobile",
        "location": "NY"
    }

print("=== API END-TO-END TEST ===")
reset_graph()

print("\n--- Sending Tx 1: A -> B ---")
r1 = client.post("/transaction", json=make_tx("A", "B", 100))
print("Response:", r1.json())

print("\n--- Sending Tx 2: B -> C ---")
r2 = client.post("/transaction", json=make_tx("B", "C", 200))
print("Response:", r2.json())

print("\n--- Sending Tx 3: C -> A (CYCLE!) ---")
r3 = client.post("/transaction", json=make_tx("C", "A", 300))
print("Response:", r3.json())

print("\n--- Checking Trace for A ---")
trace = client.get("/trace/A")
print("Trace path count:", trace.json().get("path_count"))
print("Trace payload keys:", list(trace.json().keys()))

print("\n=== TEST COMPLETE ===")
