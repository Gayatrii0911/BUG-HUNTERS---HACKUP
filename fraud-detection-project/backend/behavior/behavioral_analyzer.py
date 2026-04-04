import statistics
import datetime
from typing import Dict, Any
from backend.behavior.profile_store import get_profile

# In-memory device registry (Shared Intelligence)
_device_registry: Dict[str, Dict] = {}

def analyze_behavior(tx: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified Behavioral Intelligence Engine.
    Combines User Profiling with Global Device Intelligence.
    """
    user_id = tx.get("sender_id", "unknown")
    device_id = tx.get("device_id", "unknown")
    location = tx.get("location", "unknown")
    channel = tx.get("channel", "web")
    amount = tx.get("amount", 0.0)
    timestamp = float(tx.get("timestamp", 0.0))

    profile = get_profile(user_id)
    amounts = profile["amounts"]
    
    # 1. Profiling Intelligence (User-specific)
    deviations = {
        "amount_deviation": 0.0,
        "amount_exceeds_2x": False,
        "frequency_spike": False,
        "new_receiver": False,
        "new_device": False,
        "new_location": False,
        "new_channel": False,
        "time_deviation": False,
        "extreme_amount": amount > 50000,
        "self_transfer": user_id == tx.get("receiver_id"),
        "deviation_score": 0.0
    }

    if len(amounts) >= 1:
        avg = statistics.mean(amounts)
        if amount > (2 * avg):
            deviations["amount_exceeds_2x"] = True
        
        if len(amounts) >= 3:
            std = statistics.stdev(amounts) if len(amounts) > 1 else 1.0
            z = abs(amount - avg) / (std if std > 0 else 1.0)
            deviations["amount_deviation"] = round(z, 3)

    has_history = profile["transaction_count"] > 0
    deviations["new_receiver"] = has_history and tx.get("receiver_id") not in profile["receivers"]
    deviations["new_device"] = has_history and device_id not in profile["devices"]
    deviations["new_location"] = has_history and location not in profile["locations"]
    deviations["new_channel"] = has_history and channel not in profile["channels"]

    # Time-of-day check
    try:
        dt = datetime.datetime.fromtimestamp(timestamp)
        user_hours = sorted(profile["transaction_hours"].items(), key=lambda x: x[1], reverse=True)[:3]
        top_hours = [h for h, c in user_hours]
        if profile["transaction_count"] > 5 and dt.hour not in top_hours:
            deviations["time_deviation"] = True
            
        # Dormant account activation (Inactivity for > 300s in demo terms)
        if len(profile["timestamps"]) >= 1:
            last_ts = float(profile["timestamps"][-1])
            if (timestamp - last_ts) > 300: # 5 mins gap for demo
                 deviations["dormant_activation"] = True
    except:
        pass

    # 2. Device Intelligence (Global Registry)
    device_info = {
        "device_known": False,
        "device_user_mismatch": False,
        "impossible_travel": False,
        "suspicious_channel": channel in ["tor", "vpn", "proxy"],
        "device_risk": 0.0
    }

    if device_id in _device_registry:
        reg = _device_registry[device_id]
        device_info["device_known"] = True
        if reg.get("usual_user") != user_id:
            device_info["device_user_mismatch"] = True
        
        # Elite Impossible Travel (Location change within 5 mins)
        last_loc = reg.get("last_location")
        last_time = reg.get("last_timestamp", 0)
        if last_loc and last_loc != location:
            time_gap = timestamp - last_time
            if time_gap < 300: # Less than 5 mins between DIFFERENT locations
                device_info["impossible_travel"] = True
        
        reg["last_location"] = location
        reg["last_timestamp"] = timestamp
    else:
        _device_registry[device_id] = {
            "usual_user": user_id, 
            "last_location": location, 
            "last_timestamp": timestamp
        }

    # Final Component Scoring
    d_flags = [deviations[f] for f in ["amount_exceeds_2x", "new_device", "new_location", "time_deviation", "extreme_amount", "self_transfer"]]
    deviations["deviation_score"] = round(sum(d_flags) / len(d_flags), 3)

    dev_flags = [not device_info["device_known"], device_info["device_user_mismatch"], device_info["impossible_travel"], device_info["suspicious_channel"]]
    device_info["device_risk"] = round(sum(dev_flags) / len(dev_flags), 3)

    return {
        "deviations": deviations,
        "device_info": device_info
    }

def reset_behavior_engine():
    global _device_registry
    _device_registry = {}
