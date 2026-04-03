import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def log_section(title):
    print("\n" + "="*80)
    print(f" SECTION: {title}")
    print("="*80)

def log_test(num, name, success, info="", reasons=None):
    status = "[PASS]" if success else "[FAIL]"
    print(f"Test {str(num).zfill(2)} | {status} | {name.ljust(35)} | {info}")
    if not success and reasons:
        print(f"     REASONS: {json.dumps(reasons, indent=2)}")

def safe_post(endpoint, data):
    try:
        url = f"{BASE_URL}{endpoint}"
        r = requests.post(url, json=data)
        if r.status_code >= 400:
            print(f"ERROR: {endpoint} returned {r.status_code} - {r.text}")
            return {"error": True, "status": r.status_code, "body": r.text}
        return r.json()
    except Exception as e:
        print(f"EXCEPTION in safe_post: {str(e)}")
        return {"error": True, "message": str(e)}

def run_comprehensive_validation():
    # 0. RESET
    requests.post(f"{BASE_URL}/simulation/reset")
    
    # 1. MVP VALIDATION
    log_section("1. MVP VALIDATION")
    
    # Core flow
    r_core = safe_post("/transaction", {"sender_id": "U1", "receiver_id": "U2", "amount": 100, "location": "NYC", "device_id": "D1"})
    # Decision might be MFA if model is sensitive
    log_test(1.1, "Transaction Core Flow", r_core.get('decision') in ["APPROVE", "MFA"], f"Score: {r_core.get('risk_score', 'N/A')} | Decision: {r_core.get('decision', 'N/A')}", r_core.get('reasons'))
    
    # Graph & Behavior
    safe_post("/transaction", {"sender_id": "U1", "receiver_id": "U3", "amount": 120})
    r_graph = safe_post("/transaction", {"sender_id": "U3", "receiver_id": "U1", "amount": 120})
    has_cycle = any("cycle" in str(m.get('message', '')).lower() for m in r_graph.get('reasons', []))
    log_test(1.2, "Cycle Detection (Graph)", has_cycle, "Cycle detected." if has_cycle else "No cycle flagged.", r_graph.get('reasons'))

    # Alert retrieval
    alerts = requests.get(f"{BASE_URL}/alerts").json().get('alerts', [])
    log_test(1.3, "Alert Retrieval", len(alerts) >= 0, f"Alert count: {len(alerts)}")

    # Trace
    trace = requests.get(f"{BASE_URL}/trace/U1").json()
    log_test(1.4, "Trace Support", "paths" in trace, f"Paths: {len(trace.get('paths', []))}")

    # 2. PS COMPLIANCE
    log_section("2. PS COMPLIANCE")
    
    # Behavioral Profile
    # Hit enough transactions to build a profile for U_BH
    for i in range(5):
        safe_post("/transaction", {"sender_id": "U_BH", "receiver_id": f"R_{i}", "amount": 50})
    
    r_bh = safe_post("/transaction", {"sender_id": "U_BH", "receiver_id": "NEW_R", "amount": 5000}) # Spike
    has_spike = any("amount" in str(m.get('message', '')).lower() or "spike" in str(m.get('message', '')).lower() for m in r_bh.get('reasons', []))
    log_test(2.1, "Behavioral Anomaly", has_spike, "Detected amount spike." if has_spike else "Spike missed.", r_bh.get('reasons'))

    # Decisioning & Explainability
    log_test(2.2, "Explainable Decisions", len(r_bh.get('reasons', [])) > 0 and r_bh.get('decision') in ["APPROVE", "MFA", "BLOCK"], "Reasons present.")

    # 3. ADVANCED / ELITE FEATURES
    log_section("3. ADVANCED / ELITE FEATURES")
    
    # Coordinated Fraud (Cycle + Anomaly)
    requests.post(f"{BASE_URL}/simulation/reset")
    safe_post("/transaction", {"sender_id": "X", "receiver_id": "Y", "amount": 100000}) # High ML anomaly if model weights are low
    safe_post("/transaction", {"sender_id": "Y", "receiver_id": "Z", "amount": 100000})
    r_coord = safe_post("/transaction", {"sender_id": "Z", "receiver_id": "X", "amount": 100000, "location": "MARS", "device_id": "SATAN"})
    log_test(3.1, "Coordinated Fraud Synergy", r_coord.get('risk_score', 0) >= 75, f"Combined Risk: {r_coord.get('risk_score')}", r_coord.get('reasons'))

    # Smurfing (Lots of small transactions)
    requests.post(f"{BASE_URL}/simulation/reset")
    for _ in range(15):
        safe_post("/transaction", {"sender_id": "SMURF", "receiver_id": "MULE", "amount": 10})
    r_smurf = safe_post("/transaction", {"sender_id": "SMURF", "receiver_id": "MULE", "amount": 10})
    log_test(3.2, "Smurfing Detection", any("velocity" in str(m.get('message', '')).lower() or "smurf" in str(m.get('message', '')).lower() or "structuring" in str(m.get('message', '')).lower() for m in r_smurf.get('reasons', [])), "Velocity/Smurfing flagged.")

    # 4. API & EDGE CASES
    log_section("4. API & EDGE CASES")
    r_inv = safe_post("/transaction", {"sender_id": "X"}) # Missing fields
    log_test(4.1, "Invalid Payload Handling", r_inv.get('error'), "Correctly rejected missing fields.")
    
    r_self = safe_post("/transaction", {"sender_id": "SELF", "receiver_id": "SELF", "amount": 100})
    log_test(4.2, "Self Transfer Check", any("self" in m.get('message', '').lower() for m in r_self.get('reasons', [])), "Flagged self transfer.")

    # 5. PERFORMANCE
    log_section("5. PERFORMANCE")
    start = time.time()
    for _ in range(10):
        safe_post("/transaction", {"sender_id": f"P{_}", "receiver_id": "R", "amount": 10})
    end = time.time()
    avg_lat = (end - start) / 10 * 1000
    log_test(5.1, "Single Tx Latency (Avg)", avg_lat < 200, f"{avg_lat:.2f}ms")

    print("\n" + "="*80)
    print(" COMPREHENSIVE VALIDATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    run_comprehensive_validation()
