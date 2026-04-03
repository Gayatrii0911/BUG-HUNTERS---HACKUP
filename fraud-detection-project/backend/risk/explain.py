from typing import Dict, Any, List

def generate_explanation(
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    graph_signals: Dict[str, Any],
    anomaly_score: float,
    components: Dict[str, float],
) -> List[str]:
    reasons = []

    if deviations.get("amount_deviation", 0) > 2.5:
        reasons.append(f"Transaction amount is {deviations['amount_deviation']:.1f} standard deviations above user average")
    if deviations.get("new_receiver"):
        reasons.append("First transaction to this recipient")
    if deviations.get("new_device"):
        reasons.append("Transaction initiated from an unrecognized device")
    if deviations.get("new_location"):
        reasons.append("New geographic location detected")
    if deviations.get("frequency_spike"):
        reasons.append("Unusual transaction frequency for this user")
    if device_info.get("impossible_travel"):
        reasons.append("Device appears in a different location than expected (impossible travel)")
    if device_info.get("suspicious_channel"):
        reasons.append("Transaction routed through anonymizing network (VPN/Tor/proxy)")
    if graph_signals.get("has_cycle"):
        reasons.append("Cyclic fund flow detected in transaction graph")
    if graph_signals.get("suspicious_connections"):
        reasons.append("Account linked to flagged entities in the network")
    if anomaly_score > 0.7:
        reasons.append(f"ML anomaly detector flagged this transaction (score: {anomaly_score:.2f})")

    if not reasons:
        reasons.append("No significant risk indicators detected")

    return reasons