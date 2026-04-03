from typing import Dict, Any

def extract_features(tx: Dict[str, Any], deviations: Dict[str, Any], device_info: Dict[str, Any]) -> list:
    """Returns a flat feature vector for the ML model."""
    return [
        float(tx.get("amount", 0)),
        float(''.join(filter(str.isdigit, tx.get("sender_id", "0"))) or 0),  # extract numeric part for ML proxy
        float(deviations.get("amount_deviation", 0)),
        float(deviations.get("deviation_score", 0)),
        float(1 if deviations.get("new_receiver") else 0),
        float(1 if deviations.get("new_device") else 0),
        float(1 if deviations.get("new_location") else 0),
        float(1 if deviations.get("frequency_spike") else 0),
        float(device_info.get("device_risk", 0)),
        float(1 if device_info.get("impossible_travel") else 0),
        float(1 if device_info.get("device_user_mismatch") else 0),
        float(1 if device_info.get("suspicious_channel") else 0),
    ]