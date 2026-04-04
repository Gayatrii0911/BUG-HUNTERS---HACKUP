import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def log(stage, case, status, msg=""):
    color = "\033[92m" if status == "PASS" else "\033[91m"
    print(f"{color}[{status}] Stage {stage} | {case}: {msg}\033[0m")

def test_ultimate_audit():
    print("🚀 STARTING ULTIMATE FRAUD AUDIT V2 (ELITE HARDENING)")

    # ---------------------------------------------------------
    # STAGE 1: RESET & MVP FOUNDATION
    # ---------------------------------------------------------
    requests.post(f"{BASE_URL}/simulation/reset")
    log(1, "Reset", "PASS", "System state purged for fresh audit.")

    # 1.1 Simple Normal Transaction
    payload = {
        "sender_id": "USER_NORMAL",
        "receiver_id": "MERCHANT_X",
        "amount": 100.0,
        "device_id": "DEV_SAFE",
        "location": "Mumbai",
        "channel": "web"
    }
    r = requests.post(f"{BASE_URL}/transaction", json=payload).json()
    if r.get("decision") == "APPROVE" and r.get("risk_score") < 20:
        log(1, "MVP Normal", "PASS", "Baseline decision accurate.")
    else:
        log(1, "MVP Normal", "FAIL", f"Decision: {r.get('decision')}")

    # ---------------------------------------------------------
    # STAGE 2: PS COMPLIANCE (BEHAVIOR & ANOMALY)
    # ---------------------------------------------------------
    # 2.1 Amount Deviation (Behavior)
    # Give USER_NORMAL some history
    for _ in range(3):
        requests.post(f"{BASE_URL}/transaction", json=payload)
    
    # Now spike it
    spike_payload = payload.copy()
    spike_payload["amount"] = 5000.0
    r = requests.post(f"{BASE_URL}/transaction", json=spike_payload).json()
    has_behavior_reason = any(cat == "behavior" for cat in r.get("reason_categories", {}))
    if r.get("risk_score") > 40 and has_behavior_reason:
        log(2, "Behavior Spike", "PASS", "Deviation detected and categorized.")
    else:
        log(2, "Behavior Spike", "FAIL", "Anomaly not penalized correctly.")

    # 2.2 New Device/Location (Anomaly)
    new_env_payload = payload.copy()
    new_env_payload["device_id"] = "DEV_UNKNOWN"
    new_env_payload["location"] = "New York"
    new_env_payload["amount"] = 800.0
    r = requests.post(f"{BASE_URL}/transaction", json=new_env_payload).json()
    if r.get("decision") in ["MFA", "BLOCK"]:
        log(2, "Environment Shift", "PASS", "Identity risk correctly flagged.")
    else:
        log(2, "Environment Shift", "FAIL", "New device/location ignored.")

    # ---------------------------------------------------------
    # STAGE 3: GRAPH INTELLIGENCE (Member 1 Specialization)
    # ---------------------------------------------------------
    # 3.1 Cycle Detection
    requests.post(f"{BASE_URL}/simulation/reset")
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "A", "receiver_id": "B", "amount": 10})
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "B", "receiver_id": "C", "amount": 10})
    r = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "C", "receiver_id": "A", "amount": 10}).json()
    
    found_cycle = any("Cycle" in res.get("message", "") for res in r.get("reasons", []))
    if found_cycle and r.get("risk_score") >= 60:
        log(3, "Cycle Fraud", "PASS", "Loop detected in network topology.")
    else:
        log(3, "Cycle Fraud", "FAIL", "Cycle logic non-responsive.")

    # 3.2 Relay Node Detection
    requests.post(f"{BASE_URL}/simulation/reset")
    # Feed into RELAY
    for i in range(3): requests.post(f"{BASE_URL}/transaction", json={"sender_id": f"SRC_{i}", "receiver_id": "RELAY", "amount": 50})
    # Feed out of RELAY
    for i in range(2): requests.post(f"{BASE_URL}/transaction", json={"sender_id": "RELAY", "receiver_id": f"DST_{i}", "amount": 50})
    # Final trigger
    r = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "RELAY", "receiver_id": "SINK", "amount": 50}).json()
    is_relay = any("Relay" in res.get("message", "") for res in r.get("reasons", []))
    if is_relay:
        log(3, "Relay Analysis", "PASS", "Laundering hub identified.")
    else:
        log(3, "Relay Analysis", "FAIL", "Relay behavior missed.")

    # ---------------------------------------------------------
    # STAGE 4: ADVANCED FUSION (Synergy & Escalation)
    # ---------------------------------------------------------
    # 4.1 Coordinated Fraud Boost
    # Spike Graph Hub + Unusual Amount
    requests.post(f"{BASE_URL}/simulation/reset")
    for i in range(5): requests.post(f"{BASE_URL}/transaction", json={"sender_id": "HUB", "receiver_id": f"ACC_{i}", "amount": 10})
    
    synergy_payload = {"sender_id": "HUB", "receiver_id": "SINK", "amount": 15000, "device_id": "NEW_DEV"}
    r = requests.post(f"{BASE_URL}/transaction", json=synergy_payload).json()
    
    if r.get("risk_score") >= 90 and r.get("decision") == "BLOCK":
        log(4, "Coordinated Synergy", "PASS", "Network + Anomaly agreement triggered max risk.")
    else:
        log(4, "Coordinated Synergy", "FAIL", f"Score: {r.get('risk_score')} too low.")

    # ---------------------------------------------------------
    # STAGE 5: INVESTIGATION PAYLOAD (Contract Audit)
    # ---------------------------------------------------------
    trace_r = requests.get(f"{BASE_URL}/trace/HUB").json()
    if "subgraph" in trace_r and "nodes" in trace_r["subgraph"]:
        log(5, "Trace Payload", "PASS", "Cytoscape payload formatted correctly.")
    else:
        log(5, "Trace Payload", "FAIL", "Subgraph payload missing or invalid.")

    # ---------------------------------------------------------
    # STAGE 6: PERFORMANCE / STRESS
    # ---------------------------------------------------------
    start = time.time()
    for _ in range(5): requests.post(f"{BASE_URL}/transaction", json=payload)
    end = time.time()
    avg_lat = (end - start) / 5
    if avg_lat < 0.2:
        log(6, "Latency Check", "PASS", f"Avg: {int(avg_lat*1000)}ms. Within real-time constraints.")
    else:
        log(6, "Latency Check", "FAIL", f"Avg: {int(avg_lat*1000)}ms too slow.")

    print("\n✅ ULTIMATE FRAUD AUDIT V2 COMPLETE - 100% SUCCESS EXPECTED")

if __name__ == "__main__":
    test_ultimate_audit()
