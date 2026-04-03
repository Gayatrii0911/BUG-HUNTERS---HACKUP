from collections import defaultdict
from typing import Dict, Any

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


def get_profile(user_id: str) -> Dict[str, Any]:
    return _profiles[user_id]


def update_profile(user_id: str, tx: Dict[str, Any]):
    p = _profiles[user_id]
    p["transaction_count"] += 1
    p["total_amount"] += tx.get("amount", 0)
    p["amounts"].append(tx.get("amount", 0))
    p["timestamps"].append(tx.get("timestamp", ""))
    p["receivers"][tx.get("receiver_id", "unknown")] += 1
    p["devices"][tx.get("device_id", "unknown")] += 1
    p["locations"][tx.get("location", "unknown")] += 1
    p["channels"][tx.get("channel", "unknown")] += 1
    
    # NEW: Store hour of transaction (0-23)
    if tx.get("timestamp"):
        try:
            import datetime
            dt = datetime.datetime.fromtimestamp(float(tx["timestamp"]))
            p["transaction_hours"][dt.hour] += 1
        except:
            pass