import time
from backend.services.transaction_service import process_transaction

def run_scenario(name: str):
    """
    Executes a specific fraud scenario through the real real-time pipeline.
    """
    scenarios = {
        "normal_user": [
            {"sender_id": "User_01", "receiver_id": "Amazon", "amount": 1500, "location": "Noida", "device_id": "D_NORM"}
        ],
        "new_device_anomaly": [
            {"sender_id": "User_01", "receiver_id": "GamerStore", "amount": 15000, "location": "Bangalore", "device_id": "D_NEW"}
        ],
        "cycle_fraud": [
            {"sender_id": "RingA", "receiver_id": "RingB", "amount": 1000},
            {"sender_id": "RingB", "receiver_id": "RingC", "amount": 1000},
            {"sender_id": "RingC", "receiver_id": "RingA", "amount": 1000}
        ],
        "mule_hub": [
            *[{"sender_id": "MuleCenter", "receiver_id": f"User_{i}", "amount": 55000} for i in range(12)]
        ],
        "layering_chain": [
            {"sender_id": "Boss", "receiver_id": "L1", "amount": 5000},
            {"sender_id": "L1", "receiver_id": "L2", "amount": 5000},
            {"sender_id": "L2", "receiver_id": "L3", "amount": 5000},
            {"sender_id": "L3", "receiver_id": "L4", "amount": 5000},
            {"sender_id": "L4", "receiver_id": "Offshore", "amount": 5000}
        ],
        "smurfing": [
            {"sender_id": "Smurf", "receiver_id": "Recipient", "amount": 50} for _ in range(5)
        ],
        "account_takeover": [
            {"sender_id": "Victim", "receiver_id": "Merchant", "amount": 500, "device_id": "V_DEV"},
            {"sender_id": "Victim", "receiver_id": "Evil", "amount": 95000, "device_id": "HACKER_HW", "location": "Unknown"}
        ],
        "coordinated_synergy": [
            # Build hub
            *[{"sender_id": "BossX", "receiver_id": f"Node_{i}", "amount": 1000} for i in range(10)],
            # Cycle
            {"sender_id": "Node_0", "receiver_id": "BossX", "amount": 50000},
            # Final Boosted TX
            {"sender_id": "BossX", "receiver_id": "Target_Asset", "amount": 999999, "location": "N_KOREA", "device_id": "DARK_DEV"}
        ],
        "repeated_suspicious": [
             {"sender_id": "Repeater", "receiver_id": "A", "amount": 5000},
             {"sender_id": "Repeater", "receiver_id": "B", "amount": 5000},
             {"sender_id": "Repeater", "receiver_id": "C", "amount": 5000} # Escalation should trigger
        ]
    }

    if name not in scenarios:
        raise ValueError(f"Scenario '{name}' not found")

    results = []
    print(f"--- RUNNING SCENARIO: {name} ---")
    for tx in scenarios[name]:
        res = process_transaction(tx)
        results.append(res)
        print(f"TX {res['transaction_id']} Result: {res['decision']} (Score: {res['risk_score']})")
    
    return results
