from fastapi.testclient import TestClient
from backend.main import app
import time

client = TestClient(app)

def test_workflow():
    print("--- Testing Unified Backend ---")
    
    health = client.get("/")
    print("Root API:", health.json())

    tx1 = {
        "sender_id": "userA",
        "receiver_id": "userB",
        "amount": 100.0,
        "device_id": "device_1",
        "location": "NY"
    }

    tx2 = {
        "sender_id": "userB",
        "receiver_id": "userC",
        "amount": 250.0,
        "device_id": "device_2",
        "location": "LA"
    }

    tx3 = {
        "sender_id": "userC",
        "receiver_id": "userA", # CYCLE
        "amount": 3000.0,       # Anomaly amount
        "device_id": "device_3_UNKNOWN",
        "location": "MOSCOW"
    }

    print("\nSending Tx1:")
    r1 = client.post("/transaction", json=tx1)
    print(r1.json())

    print("\nSending Tx2:")
    r2 = client.post("/transaction", json=tx2)
    print(r2.json())

    print("\nSending Tx3 (Fraud Simulation):")
    r3 = client.post("/transaction", json=tx3)
    print(r3.json())

    print("\nGetting Alerts:")
    alerts = client.get("/alerts")
    print(alerts.json())

if __name__ == "__main__":
    test_workflow()
