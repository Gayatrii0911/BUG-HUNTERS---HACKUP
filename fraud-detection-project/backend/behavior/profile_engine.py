import statistics
from typing import Dict, Any
from backend.behavior.profile_store import get_profile


def compute_deviations(user_id: str, tx: Dict[str, Any]) -> Dict[str, Any]:
    profile = get_profile(user_id)
    amounts = profile["amounts"]
    result = {
        "amount_deviation": 0.0,
        "amount_exceeds_2x": False,
        "frequency_spike": False,
        "new_receiver": False,
        "new_device": False,
        "new_location": False,
        "new_channel": False,
        "time_deviation": False,
        "self_transfer": user_id == tx.get("receiver_id"),
        "avg_amount": 0.0,
        "current_amount": tx.get("amount", 0.0),
        "deviation_score": 0.0,
    }
    
    if len(amounts) >= 1:
        avg = statistics.mean(amounts)
        result["avg_amount"] = round(avg, 2)
        if tx.get("amount", 0) > (2 * avg):
            result["amount_exceeds_2x"] = True
    
    if len(amounts) >= 3:
        avg = statistics.mean(amounts)
        std = statistics.stdev(amounts) if len(amounts) > 1 else 1.0
        if std == 0:
            std = 1.0
        z = abs(tx.get("amount", 0) - avg) / std
        result["amount_deviation"] = round(z, 3)
    
    # Frequency logic: Flag if more than 3 transactions in last 5 minutes (mocked via count for now)
    if profile["transaction_count"] > 10:
        # Simplistic spike: if they usually have 1/day but suddenly have 5 in a row
        result["frequency_spike"] = profile["transaction_count"] % 7 == 0

    has_history = profile["transaction_count"] > 0
    result["new_receiver"] = has_history and tx.get("receiver_id") not in profile["receivers"]
    result["new_device"] = has_history and tx.get("device_id") not in profile["devices"]
    result["new_location"] = has_history and tx.get("location") not in profile["locations"]
    result["new_channel"] = has_history and tx.get("channel") not in profile["channels"]

    # Time-of-day check
    try:
        import datetime
        dt = datetime.datetime.fromtimestamp(float(tx.get("timestamp", 0)))
        user_hours = sorted(profile["transaction_hours"].items(), key=lambda x: x[1], reverse=True)[:3]
        top_hours = [h for h, c in user_hours]
        if profile["transaction_count"] > 5 and dt.hour not in top_hours:
            result["time_deviation"] = True
    except:
        pass

    flags = [
        result["amount_deviation"] > 2.5,
        result["amount_exceeds_2x"],
        result["frequency_spike"],
        result["new_receiver"],
        result["new_device"],
        result["new_location"],
        result["new_channel"],
        result["time_deviation"],
        result["self_transfer"],
    ]
    result["deviation_score"] = round(sum(flags) / len(flags), 3)
    return result