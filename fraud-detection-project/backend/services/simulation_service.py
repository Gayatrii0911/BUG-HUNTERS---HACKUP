import time
from backend.services.transaction_service import process_transaction

def run_scenario(name: str):
    """
    Executes a specific fraud scenario through the real real-time pipeline.
    """
    scenarios = {
        "normal": [
            {"sender_id": "User_01", "receiver_id": "Amazon", "amount": 1500, "location": "Noida", "device_id": "D_NORM"}
        ],
        "cold_start": [
             {"sender_id": "NEW_USER_STRESS", "receiver_id": "U2", "amount": 1500, "location": "Delhi"}
        ],
        "fractal_cycle": [
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
            {"sender_id": "Smurf", "receiver_id": "Recipient", "amount": 50, "device_id": "S_DEV"} for _ in range(5)
        ],
        "account_takeover": [
            {"sender_id": "Victim", "receiver_id": "Merchant", "amount": 500, "device_id": "V_DEV"},
            {"sender_id": "Victim", "receiver_id": "Evil", "amount": 95000, "device_id": "HACKER_HW", "location": "Unknown"}
        ],
        "big_transaction": [
            {"sender_id": "Whale_User", "receiver_id": "Offshore_Account", "amount": 2500000, "location": "Dubai", "device_id": "UNKNOWN_DEV"}
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
        ],
        "nexus_live": [
            # High Volume Legitimate Traffic
            {"sender_id": "User_PX", "receiver_id": "Zomato", "amount": 450, "location": "Bangalore", "device_id": "D_ANDR_1"},
            {"sender_id": "User_PX", "receiver_id": "Amazon_IN", "amount": 12500, "location": "Bangalore", "device_id": "D_ANDR_1"},
            {"sender_id": "User_MK", "receiver_id": "Reliance_Fresh", "amount": 3200, "location": "Mumbai", "device_id": "D_IOS_9"},
            {"sender_id": "User_SK", "receiver_id": "Uber_India", "amount": 890, "location": "Delhi", "device_id": "D_ANDR_X"},
            
            # Subtle Smurfing (Low amounts, high frequency)
            *[{"sender_id": "SmurfNode", "receiver_id": "LaunderTarget", "amount": 150, "device_id": "S_BOT_7"} for _ in range(8)],
            
            # Velocity Attack (Fast repeated hits)
            *[{"sender_id": "Hacker_X", "receiver_id": "Victim_A", "amount": 95000, "location": "Ukraine", "device_id": "PROXY_HW"} for _ in range(4)],
            
            # Complex Ring (Multi-hop)
            {"sender_id": "Ring_Leader", "receiver_id": "Node_1", "amount": 500000},
            {"sender_id": "Node_1", "receiver_id": "Node_2", "amount": 490000},
            {"sender_id": "Node_2", "receiver_id": "Node_3", "amount": 485000},
            {"sender_id": "Node_3", "receiver_id": "Ring_Leader", "amount": 480000}, # Cycle detection
            
            # Geographic Anomaly
            {"sender_id": "Regular_User", "receiver_id": "Local_Shop", "amount": 50, "location": "Pune", "device_id": "D_PUNE_1"},
            {"sender_id": "Regular_User", "receiver_id": "Casino_Global", "amount": 99000, "location": "Macau", "device_id": "UNKNOWN_HW"}
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
