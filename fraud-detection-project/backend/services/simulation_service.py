import random
import time
import uuid
from backend.services.transaction_service import process_transaction

class SimulationService:
    @staticmethod
    def run_normal_wave(count: int = 10):
        """Simulates a batch of normal, low-risk transactions."""
        print(f"[Simulation] Running Normal Wave ({count} tx)...")
        results = []
        for i in range(count):
            tx = {
                "sender_id": f"user_{random.randint(100, 200)}",
                "receiver_id": f"user_{random.randint(300, 400)}",
                "amount": round(random.uniform(10, 500), 2),
                "device_id": f"device_{random.randint(1, 50)}",
                "location": random.choice(["New York", "London", "Mumbai", "Tokyo"]),
                "channel": "web"
            }
            results.append(process_transaction(tx))
        return results

    @staticmethod
    def run_ato_attack():
        """Simulates an Account Takeover (ATO) pattern."""
        print("[Simulation] Running ATO Attack...")
        user_id = "victim_99"
        # 1. Warm up profile with a normal txn
        process_transaction({
            "sender_id": user_id,
            "receiver_id": "friend_1",
            "amount": 50.0,
            "device_id": "safe_laptop",
            "location": "New York",
            "channel": "web"
        })
        
        # 2. The Attack: New device, new location, high amount
        attack_tx = {
            "sender_id": user_id,
            "receiver_id": "attacker_wallet",
            "amount": 5000.0,
            "device_id": "stolen_phone_xyz",
            "location": "Unknown_Proxy",
            "channel": "tor"
        }
        return [process_transaction(attack_tx)]

    @staticmethod
    def run_fraud_ring(size: int = 5):
        """Simulates a coordinated fraud ring (chain of transfers)."""
        print(f"[Simulation] Running Fraud Ring (Size: {size})...")
        results = []
        # Create a chain: A -> B -> C -> D -> E
        nodes = [f"bot_{i}" for i in range(size)]
        for i in range(len(nodes) - 1):
            tx = {
                "sender_id": nodes[i],
                "receiver_id": nodes[i+1],
                "amount": 1000.0,
                "device_id": "shared_fraud_server",
                "location": "Global",
                "channel": "api"
            }
            results.append(process_transaction(tx))
        return results
