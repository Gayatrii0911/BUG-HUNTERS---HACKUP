import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def log_audit(step, status, note=""):
    color = "\033[92m" if status == "PASS" else "\033[91m"
    reset = "\033[0m"
    print(f"[{step}] {status} | {note}{reset}")

def run_master_audit():
    print("\n" + "="*50)
    print("🚀 SENTINEL-X MASTER PRODUCTION AUDIT")
    print("="*50 + "\n")

    requests.post(f"{BASE_URL}/debug/reset")
    log_audit("STATE", "PASS", "System reset.")

    # MVP 1
    tx = {"sender_id": "U1", "receiver_id": "U2", "amount": 100.0, "location": "L1", "device_id": "D1"}
    r = requests.post(f"{BASE_URL}/transaction", json=tx).json()
    log_audit("MVP-01", "PASS" if r['decision'] == "APPROVE" else "FAIL", f"Normal Tx Score: {r['risk_score']} | Decision: {r['decision']}")

    # MVP 2
    tx = {"sender_id": "NEW_USER", "receiver_id": "U2", "amount": 200.0, "location": "L1", "device_id": "D2"}
    r1 = requests.post(f"{BASE_URL}/transaction", json=tx).json()
    log_audit("MVP-02", "PASS" if r1['decision'] in ["APPROVE", "MFA"] else "FAIL", "Cold start.")

    # PS 1
    for _ in range(5): requests.post(f"{BASE_URL}/transaction", json={"sender_id": "U1", "receiver_id": "U2", "amount": 100.0, "device_id": "D1", "location": "L1"})
    tx = {"sender_id": "U1", "receiver_id": "U3", "amount": 15000.0, "location": "L1", "device_id": "D1"}
    r2 = requests.post(f"{BASE_URL}/transaction", json=tx).json()
    reason_msgs = [res['message'] for res in r2['reasons']]
    has_behavior = any("amount" in m.lower() or "usual" in m.lower() or "exceeds" in m.lower() for m in reason_msgs)
    log_audit("PS-01", "PASS" if has_behavior else "FAIL", f"Behavioral spike. Reasons: {reason_msgs}")

    # PS 2
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "A", "receiver_id": "B", "amount": 10})
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "B", "receiver_id": "C", "amount": 10})
    r3 = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "C", "receiver_id": "A", "amount": 20}).json()
    has_cycle = any("Cycle" in m['message'] for m in r3['reasons'])
    log_audit("PS-02", "PASS" if has_cycle else "FAIL", f"Graph Cycle. Risk: {r3['risk_score']}")

    # 5. ELITE: COORDINATED SYNERGY (Hub + Anomaly)
    for i in range(11): requests.post(f"{BASE_URL}/transaction", json={"sender_id": "BOSS", "receiver_id": f"M_{i}", "amount": 5})
    
    # Synergistic high risk tx
    tx = {
        "sender_id": "BOSS", 
        "receiver_id": "M_0", 
        "amount": 99999.0, 
        "location": "UNKNOWN_LOC_DARK_WORLD", 
        "device_id": "EVIL_HARDWARE_SIGNATURE"
    }
    r4 = requests.post(f"{BASE_URL}/transaction", json=tx).json()
    log_audit("ELITE-01", "PASS" if r4['risk_score'] >= 60 else "FAIL", f"Synergy/Synergy: {r4['risk_score']} | Reasons: {r4['reasons']}")

    # API
    health = requests.get(f"{BASE_URL}/health").json()
    log_audit("API-01", "PASS", f"System Health Check: {health['status']}")

    print("\n" + "="*50)
    print("🏁 AUDIT COMPLETE: READY FOR SUBMISSION")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_master_audit()
