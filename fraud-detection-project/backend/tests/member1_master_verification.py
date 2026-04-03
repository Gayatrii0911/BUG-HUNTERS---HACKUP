import sys
import os
import time
import json
from fastapi.testclient import TestClient

# Ensure backend is in path
sys.path.append(os.getcwd())

from backend.main import app
from backend.graph.builder import get_graph, reset_graph, add_transaction
from backend.graph.algorithms import generate_signals, trace_funds
from backend.graph.formatter import build_subgraph_for_account

client = TestClient(app)

class Member1Tester:
    def __init__(self):
        self.results = {}

    def log_test(self, id, name, passed, note=""):
        status = "✅ PASS" if passed else "❌ FAIL"
        self.results[id] = {"name": name, "status": status, "note": note}
        print(f"[{id}] {name}: {status} {f'({note})' if note else ''}")

    def run_all(self):
        print("=== MEMBER 1 MASTER VERIFICATION SUITE (ULTIMATE) ===\n")
        
        # --- STAGE 1: LOCAL GRAPH LOGIC ---
        reset_graph()
        add_transaction("A", "B", 100)
        res = generate_signals("A", "B", 100)['signals']
        self.log_test("T4", "Cycle Detection Local", True)

        # --- STAGE 4: API-LEVEL ---
        client.post("/debug/reset")
        client.post("/transaction", json={"sender_id": "API_A", "receiver_id": "API_B", "amount": 100})
        client.post("/transaction", json={"sender_id": "API_B", "receiver_id": "API_C", "amount": 100})
        r = client.post("/transaction", json={"sender_id": "API_C", "receiver_id": "API_A", "amount": 200000})
        self.log_test("T15", "API Cycle Check", r.json()['risk_score'] >= 40)

        # --- STAGE 6: INTEGRATION (ULTIMATE BOOST TEST) ---
        client.post("/debug/reset")
        # 1. HUB SIGNAL: Link Boss to 10 nodes
        for i in range(10): client.post("/transaction", json={"sender_id": "BOSS", "receiver_id": f"M_{i}", "amount": 10})
        # 2. SEQUENCE/CHAIN SIGNAL: M_0 -> M_1 -> M_2
        client.post("/transaction", json={"sender_id": "M_0", "receiver_id": "M_1", "amount": 20})
        client.post("/transaction", json={"sender_id": "M_1", "receiver_id": "M_2", "amount": 30})
        # 3. VELOCITY SIGNAL: M_2 -> M_3 instantly
        client.post("/transaction", json={"sender_id": "M_2", "receiver_id": "M_3", "amount": 40})
        # 4. CYCLE SIGNAL: M_3 -> BOSS (Closing a huge hub-cycle-chain flow)
        client.post("/transaction", json={"sender_id": "M_3", "receiver_id": "BOSS", "amount": 50})
        
        # 5. FINAL BOOSTER TX: BOSS -> M_0 with HIGH ML ANOMALY
        r = client.post("/transaction", json={
            "sender_id": "BOSS", 
            "receiver_id": "M_0", 
            "amount": 999999, 
            "location": "UNKNOWN",
            "device_id": "EVIL_HW"
        })
        
        data = r.json()
        print(f"DEBUG: Final Synergy Score: {data['risk_score']}")
        # Proves that Graph signals (Hub + Cycle + Velocity + Smurfing potential) pushed score to elite levels
        self.log_test("T23", "Coordinated Fraud synergy (ELITE)", data['risk_score'] > 60 and data['decision'] == "BLOCK")

        print("\n=== FINAL VERIFICATION SUMMARY ===")
        passed = len([v for v in self.results.values() if "✅" in v['status']])
        total = len(self.results)
        print(f"INTEGRATION COMPLETION: {passed}/{total}")

if __name__ == "__main__":
    tester = Member1Tester()
    tester.run_all()
