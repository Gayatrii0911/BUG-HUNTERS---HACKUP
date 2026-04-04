from collections import defaultdict
from typing import Dict, Any, List

# Core Per-User Behavioral Memory
_profiles: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
    "transaction_count": 0,
    "total_amount": 0.0,
    "amounts": [],
    "timestamps": [],
    "receivers": defaultdict(int),
    "devices": defaultdict(int),
    "locations": defaultdict(int),
    "channels": defaultdict(int),
    "transaction_hours": defaultdict(int),
    "recent_risk_scores": [],
})

# Cross-User Device Integrity (Synthetic Identity Check)
_device_history: Dict[str, set] = defaultdict(set)

def get_profile(user_id: str) -> Dict[str, Any]:
    return _profiles[user_id]

def get_all_profiles() -> Dict[str, Any]:
    return dict(_profiles)

def reset_profiles():
    """Wipes all behavioral profiles from memory."""
    _profiles.clear()
    _device_history.clear()

def get_device_users(device_id: str) -> List[str]:
    """Returns all user IDs associated with a specific hardware fingerprint."""
    return list(_device_history.get(device_id, set()))

def update_profile(user_id: str, tx: Dict[str, Any]):
    p = _profiles[user_id]
    p["transaction_count"] += 1
    p["total_amount"] += tx.get("amount", 0)
    p["amounts"].append(tx.get("amount", 0))
    p["timestamps"].append(tx.get("timestamp", ""))
    
    receiver_id = tx.get("receiver_id", "unknown")
    device_id = tx.get("device_id", "unknown")
    location = tx.get("location", "unknown")
    channel = tx.get("channel", "unknown")

    p["receivers"][receiver_id] += 1
    p["devices"][device_id] += 1
    p["locations"][location] += 1
    p["channels"][channel] += 1
    
    # Store hardware relationship
    if device_id != "unknown":
        _device_history[device_id].add(user_id)
    
    # Store temporal pattern
    if tx.get("timestamp"):
        try:
            import datetime
            dt = datetime.datetime.fromtimestamp(float(tx["timestamp"]))
            p["transaction_hours"][dt.hour] += 1
        except:
            pass