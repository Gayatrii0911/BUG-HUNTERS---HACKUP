import statistics
from typing import Dict, Any
from backend.behavior.profile_store import get_profile


def compute_deviations(user_id: str, tx: Dict[str, Any]) -> Dict[str, Any]:
    profile = get_profile(user_id)
    amounts = profile["amounts"]
    result = {
        "amount_deviation": 0.0,
        "frequency_spike": False,
        "new_receiver": False,
        "new_device": False,
        "new_location": False,
        "new_channel": False,
        "deviation_score": 0.0,
    }
    if len(amounts) >= 3:
        avg = statistics.mean(amounts)
        std = statistics.stdev(amounts) if len(amounts) > 1 else 1.0
        if std == 0:
            std = 1.0
        z = abs(tx.get("amount", 0) - avg) / std
        result["amount_deviation"] = round(z, 3)
    if profile["transaction_count"] > 0:
        result["frequency_spike"] = profile["transaction_count"] % 5 == 0
    result["new_receiver"] = tx.get("receiver_id") not in profile["receivers"]
    result["new_device"] = tx.get("device_id") not in profile["devices"]
    result["new_location"] = tx.get("location") not in profile["locations"]
    result["new_channel"] = tx.get("channel") not in profile["channels"]
    flags = [
        result["amount_deviation"] > 2.5,
        result["frequency_spike"],
        result["new_receiver"],
        result["new_device"],
        result["new_location"],
        result["new_channel"],
    ]
    result["deviation_score"] = round(sum(flags) / len(flags), 3)
    return result