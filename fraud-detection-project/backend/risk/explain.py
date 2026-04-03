from typing import Dict, Any, List

def generate_explanation(
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    graph_signals: Dict[str, Any],
    anomaly_result: Dict[str, Any],
    recent_scores: List[float] = None
) -> List[str]:
    reasons = []
    
    # 1. Behavioral (Specific)
    amount = deviations.get("amount", 0)
    avg = deviations.get("avg_amount", 0)
    if deviations.get("amount_deviation", 0) > 2.5:
        reasons.append(f"Transaction amount Rs {amount:,} significantly exceeds user average Rs {avg:,}")
    
    if deviations.get("time_deviation"):
        import datetime
        try:
            dt = datetime.datetime.fromtimestamp(float(deviations.get("timestamp", 0)))
            reasons.append(f"Transaction at {dt.strftime('%I %p')} is unusual for this user's pattern")
        except:
            reasons.append("Transaction time is unusual for this user")

    if deviations.get("new_device"):
        reasons.append(f"Login from a new device (Device ID: {deviations.get('device_id', 'Unknown')})")
    
    if deviations.get("new_location"):
        reasons.append(f"Transaction from new location: {deviations.get('location', 'Unknown')}")

    # 2. Device/Network
    if device_info.get("impossible_travel"):
        reasons.append("Impossible travel detected (Device active in multiple locations simultaneously)")
    
    if device_info.get("suspicious_channel"):
        reasons.append("Transaction routed through anonymizing network (VPN/Tor/Proxy)")

    # 3. Graph
    if graph_signals.get("has_cycle"):
        reasons.append("Cyclic fund flow detected (Possible layering/money laundering)")
    
    conn_count = graph_signals.get("connections", 0)
    if conn_count > 5:
        reasons.append(f"Account connected to {conn_count} suspicious nodes in transaction graph")

    # 4. ML / Anomaly
    score = anomaly_result.get("anomaly_score", 0)
    level = anomaly_result.get("anomaly_level", "LOW")
    if level != "LOW":
        reasons.append(f"Anomaly score {score:.2f} ({level}) exceeds safe threshold")

    # 5. Chain Detection / Intelligence
    if (deviations.get("new_device") or device_info.get("impossible_travel")) and level == "HIGH":
        reasons.append("Suspicious login followed by abnormal transaction indicates possible account takeover")
    
    if recent_scores and len([s for s in recent_scores if s > 50]) >= 2:
        reasons.append("Repeated suspicious activity detected in recent transactions")

    if not reasons:
        reasons.append("Transaction characteristics align with historical behavioral profile")

    return reasons