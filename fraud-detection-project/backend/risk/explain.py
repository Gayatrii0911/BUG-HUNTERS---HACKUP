def generate_reasons(graph_result: dict, ml_result: dict, risk_score: float) -> list:
    reasons = []

    if graph_result.get("cycle"):
        reasons.append("Cycle detected in transaction graph")
    if graph_result.get("rapid_chain"):
        reasons.append("Rapid chain of transactions detected")
    connections = graph_result.get("connections", 0)
    if connections > 5:
        reasons.append(f"Account has unusually high connections ({connections})")
    elif connections > 2:
        reasons.append(f"Account connected to multiple accounts ({connections})")

    anomaly = ml_result.get("anomaly_score", 0)
    if anomaly > 0.8:
        reasons.append("High anomaly score detected")
    elif anomaly > 0.5:
        reasons.append("Moderate anomaly in transaction pattern")

    if not ml_result.get("device_known", True):
        reasons.append("Transaction from unrecognized device")
    if not ml_result.get("location_known", True):
        reasons.append("Transaction from unusual location")

    for r in ml_result.get("behavior_reasons", []):
        reasons.append(r)

    if not reasons:
        reasons.append("Transaction appears normal")

    return reasons