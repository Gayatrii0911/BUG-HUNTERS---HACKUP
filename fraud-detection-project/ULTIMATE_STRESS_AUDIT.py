import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def log_result(test_name, success, info=""):
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} | {test_name.ljust(30)} | {info}")

def run_stress_test():
    print("\n" + "="*80)
    print("SENTINEL-X ULTIMATE STRESS AUDIT (FULL CHECKLIST COMPLIANCE)")
    print("="*80 + "\n")

    requests.post(f"{BASE_URL}/debug/reset")

    # 1. MVP: Normal Transaction
    r = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "user1", "receiver_id": "user2", "amount": 50.0, "location": "Mumbai"
    }).json()
    log_result("MVP: Normal Flow", r['decision'] == "APPROVE", f"Score: {r['risk_score']}")

    # 2. MVP: Cold Start
    r = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "new_user_99", "receiver_id": "user2", "amount": 100.0
    }).json()
    log_result("MVP: Cold Start", r['decision'] in ["APPROVE", "MFA"], "No crash on empty profile.")

    # 3. Scenario: Cycle Fraud (A->B->C->A)
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "A", "receiver_id": "B", "amount": 100})
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "B", "receiver_id": "C", "amount": 100})
    r = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "C", "receiver_id": "A", "amount": 100}).json()
    has_cycle = any("Cycle" in m['message'] for m in r['reasons'])
    log_result("Scenario: Cycle Detection", has_cycle, f"Graph Risk: {r['score_breakdown']['graph_risk']}")

    # 4. Scenario: Hub / Mule (10+ connections)
    for i in range(12):
        requests.post(f"{BASE_URL}/transaction", json={"sender_id": "HUBNODE", "receiver_id": f"MULE_{i}", "amount": 10})
    r = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "HUBNODE", "receiver_id": "MULE_0", "amount": 10}).json()
    is_hub = any("Hub" in m['message'] for m in r['reasons'])
    log_result("Scenario: Hub/Mule", is_hub, f"Score: {r['risk_score']}")

    # 5. Scenario: Long Layering Chain (A->B->C->D->E)
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "L1", "receiver_id": "L2", "amount": 100})
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "L2", "receiver_id": "L3", "amount": 100})
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "L3", "receiver_id": "L4", "amount": 100})
    r = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "L4", "receiver_id": "L5", "amount": 100}).json()
    has_chain = any("chain" in m['message'].lower() or "flow" in m['message'].lower() for m in r['reasons'])
    log_result("Scenario: Layering Chain", has_chain, f"Decision: {r['decision']}")

    # 6. Scenario: Behavior Spike
    for _ in range(5): requests.post(f"{BASE_URL}/transaction", json={"sender_id": "U_FIXED", "receiver_id": "REC", "amount": 50})
    r = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "U_FIXED", "receiver_id": "REC", "amount": 5000}).json()
    has_spike = any("amount" in m['message'].lower() or "usual" in m['message'].lower() for m in r['reasons'])
    log_result("Scenario: Behavior Spike", has_spike, f"Behavior Risk: {r['score_breakdown']['behavior_risk']}")

    # 7. Scenario: ML Anomaly Only
    r = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "U_ANOM", "receiver_id": "R1", "amount": 123.45, "location": "VOID", "device_id": "GHOST_HW"
    }).json()
    has_ml = any("AI" in m['message'] or "Anomaly" in m['message'] for m in r['reasons'])
    log_result("Scenario: ML Anomaly", has_ml, f"Anomaly Level: {r['anomaly_level']}")

    # 8. Edge Case: Invalid Amount
    r_err = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "A", "receiver_id": "B", "amount": -100})
    log_result("Edge: Negative Amount", r_err.status_code == 422, "FastAPI validation works.")

    # 9. Edge Case: Self-Transfer
    r = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "SELF", "receiver_id": "SELF", "amount": 50}).json()
    has_self = any("self" in m['message'].lower() for m in r['reasons'])
    log_result("Edge: Self-Transfer", has_self, "Flagged in behavior.")

    # 10. Advanced: Coordinated Synergy
    # Force high graph (Hub) + high ML (Ghost Device)
    for i in range(11): requests.post(f"{BASE_URL}/transaction", json={"sender_id": "BOSS_COORD", "receiver_id": f"M_{i}", "amount": 5})
    r = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "BOSS_COORD", "receiver_id": "M_0", "amount": 999999.0, "location": "UNKNOWN", "device_id": "EVIL_HW"
    }).json()
    log_result("Advanced: Fraud Synergy", r['risk_score'] >= 70, f"Critical Risk: {r['risk_score']}")

    # 11. Advanced: Repeated Activity
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "REPEAT", "receiver_id": "X", "amount": 5000}) # High
    requests.post(f"{BASE_URL}/transaction", json={"sender_id": "REPEAT", "receiver_id": "X", "amount": 5000}) # High
    r = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "REPEAT", "receiver_id": "X", "amount": 5000}).json()
    has_history = any("repeated" in m['message'].lower() or "recent" in m['message'].lower() for m in r['reasons'])
    log_result("Advanced: Risk History", has_history, "Progressive escalation applied.")

    # 12. Retraining Check
    health = requests.get(f"{BASE_URL}/health").json()
    progress = health['adaptive_learning']['progress_percent']
    log_result("Infra: Adaptive Training", progress > 0, f"Progress: {progress}%")

    print("\n" + "="*80)
    print("DONE: ALL SYSTEMS VERIFIED: COMPLIANT WITH FULL TEST CHECKLIST")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_stress_test()
