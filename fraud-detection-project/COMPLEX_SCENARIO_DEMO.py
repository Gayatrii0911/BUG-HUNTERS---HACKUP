import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def log(scenario, status, msg=""):
    color = "\033[93m" if status == "TEST" else "\033[92m" if status == "PASS" else "\033[91m"
    print(f"{color}[{status}] {scenario}: {msg}\033[0m")

def run_complex_demo():
    print("STARTING ELITE COMPLEX SCENARIO DEMO (FOR JUDGES)")
    requests.post(f"{BASE_URL}/simulation/reset")

    # 1: Impossible Travel (Identity + Time Speed)
    log("SCENARIO 1", "TEST", "Testing Impossible Travel (Mumbai -> New York in 10s)")
    requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "VICTIM_001", "receiver_id": "BOB", "amount": 100,
        "device_id": "PHONE_X", "location": "Mumbai", "timestamp": str(time.time())
    })
    time.sleep(2)
    res = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "VICTIM_001", "receiver_id": "HACKER", "amount": 500,
        "device_id": "PHONE_X", "location": "New York", "timestamp": str(time.time())
    }).json()
    
    if "Impossible travel" in [r["message"] for r in res.get("reasons", [])]:
        log("SCENARIO 1", "PASS", "Identity theft flagged via Impossible Travel detection.")
    else:
        log("SCENARIO 1", "FAIL", "Impossible Travel was NOT detected.")

    # 2: Sophisticated Money Laundering (Smurfing -> Relay -> Sink)
    log("SCENARIO 2", "TEST", "Testing Layered Laundering (6 Source Nodes -> Relay -> Final Sink)")
    for i in range(4):
        requests.post(f"{BASE_URL}/transaction", json={"sender_id": f"SRC_{i}", "receiver_id": "RELAY", "amount": 50})
    
    # Trigger Relay
    res = requests.post(f"{BASE_URL}/transaction", json={"sender_id": "RELAY", "receiver_id": "SINK_001", "amount": 180}).json()
    
    reasons = [r["message"] for r in res.get("reasons", [])]
    if any("Relay" in r for r in reasons) or any("Multi-hop" in r for r in reasons):
        log("SCENARIO 2", "PASS", "Complex laundering chain with Relay behavior identified.")
    else:
        log("SCENARIO 2", "FAIL", "Laundering topology missed.")

    # 3: Account Takeover (New Device + Night Time + High Amount)
    log("SCENARIO 3", "TEST", "Testing Account Takeover (New Device + Unusual Amount + Night Hour)")
    # Set history first
    for _ in range(5):
        requests.post(f"{BASE_URL}/transaction", json={
            "sender_id": "USER_OLD", "receiver_id": "SAFE", "amount": 10,
            "device_id": "OLD_PHONE", "timestamp": "1712170000" # Afternoon
        })
    
    # Attack at 3 AM (1712120000 approx) on NEW Device
    res = requests.post(f"{BASE_URL}/transaction", json={
        "sender_id": "USER_OLD", "receiver_id": "UNKNOWN_BADDIE", "amount": 8000,
        "device_id": "HACKER_LAPTOP", "timestamp": "1712120000"
    }).json()

    if res["decision"] in ["BLOCK", "MFA"] and res["fraud_chain_detected"]:
        log("SCENARIO 3", "PASS", "ATO (Account Takeover) chain triggered and explained via Hybrid ML.")
    else:
        log("SCENARIO 3", "FAIL", f"ATO check failed. Decision: {res['decision']}")

    print("\nCOMPLEX DEMO VALIDATION READY FOR PRESENTATION")

if __name__ == "__main__":
    run_complex_demo()
