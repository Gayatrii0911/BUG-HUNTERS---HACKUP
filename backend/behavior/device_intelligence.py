from typing import Dict, Any

# In-memory device registry — replace with DB in prod
_device_registry: Dict[str, Dict] = {}

def analyze_device(tx: Dict[str, Any]) -> Dict[str, Any]:
    device_id = tx.get("device_id", "")
    user_id = tx.get("sender_id", "")
    location = tx.get("location", "")
    channel = tx.get("channel", "web")

    result = {
        "device_known": False,
        "device_user_mismatch": False,
        "impossible_travel": False,
        "suspicious_channel": False,
        "device_risk": 0.0,
    }

    if device_id in _device_registry:
        reg = _device_registry[device_id]
        result["device_known"] = True
        if reg.get("usual_user") != user_id:
            result["device_user_mismatch"] = True
        if reg.get("last_location") and reg["last_location"] != location:
            result["impossible_travel"] = True  # simplification; add geo distance in prod
    else:
        _device_registry[device_id] = {
            "usual_user": user_id,
            "last_location": location,
            "channel": channel,
        }

    result["suspicious_channel"] = channel in ["tor", "vpn", "proxy"]

    flags = [
        not result["device_known"],
        result["device_user_mismatch"],
        result["impossible_travel"],
        result["suspicious_channel"],
    ]
    result["device_risk"] = round(sum(flags) / len(flags), 3)

    # Update registry
    _device_registry[device_id]["last_location"] = location
    return result