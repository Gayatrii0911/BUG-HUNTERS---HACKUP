from typing import Dict, Any

def extract_features(tx: Dict[str, Any], deviations: Dict[str, Any], device_info: Dict[str, Any], graph_signals: Dict[str, Any] = None) -> list:
    """
    Elite Feature Extraction:
    Converts behavioral, device, and network-level (Graph) signals into a 14-dimensional 
    numerical vector for high-fidelity ML inference.
    """
    g = graph_signals or {}
    return [
        float(tx.get("amount", 0)),
        float(''.join(filter(str.isdigit, tx.get("sender_id", "0"))) or 0),
        float(deviations.get("amount_deviation", 0)),
        float(deviations.get("deviation_score", 0)),
        float(1 if deviations.get("new_receiver") else 0),
        float(1 if deviations.get("new_device") else 0),
        float(1 if deviations.get("new_location") else 0),
        float(1 if deviations.get("frequency_spike") else 0),
        float(device_info.get("device_risk", 0)),
        float(1 if device_info.get("impossible_travel") else 0),
        float(1 if device_info.get("device_user_mismatch") else 0),
        # Graph-Aware Features (Advanced Recommendation)
        float(g.get("graph_risk", 0) / 100.0),
        float(g.get("connections", 0) / 10.0),
        float(1 if g.get("has_cycle") else 0)
    ]