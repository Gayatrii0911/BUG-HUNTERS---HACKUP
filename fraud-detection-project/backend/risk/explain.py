from typing import Dict, Any, List

def generate_explanation(
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    graph_signals: Dict[str, Any],
    risk_result: Dict[str, Any],
    recent_scores: List[float] = None,
    identity_signals: Dict[str, Any] = None
) -> List[str]:
    reasons = []
    
    # 1. Behavioral (Specific)
    amount = deviations.get("amount", 0)
    avg = deviations.get("avg_amount", 0)
    if deviations.get("amount_deviation", 0) > 2.5:
        reasons.append(f"Transaction amount Rs {amount:,} significantly exceeds user average Rs {avg:,}")
    
    if deviations.get("time_deviation"):
        reasons.append("Transaction time is unusual for this user's historic profile")

    if deviations.get("new_device"):
        reasons.append(f"Login from a new hardware fingerprint (Device ID: {deviations.get('device_id', 'Unlisted')})")
    
    if deviations.get("new_location"):
        reasons.append(f"Transaction from geographic location mismatch: {deviations.get('location', 'Unknown')}")

    # 2. Device/Network Intelligence
    if device_info.get("impossible_travel"):
        reasons.append("Impossible travel detected (Dual location activity within physical limits)")
    
    if device_info.get("suspicious_channel"):
        reasons.append("Transaction routed through metadata-obfuscating network (VPN/Tor)")

    # 3. Graph Intelligence (Elite Hops & Flows)
    if graph_signals.get("has_cycle"):
        reasons.append("Circular fund flow detected (Money Laundering Ring)")
    
    if graph_signals.get("is_hub"):
        reasons.append(f"Account flagged as 'Hub' (Connected to {graph_signals.get('connections', 0)} entities in graph)")

    if graph_signals.get("suspicious_chain"):
        reasons.append("Money laundering chain detected (Multi-hop fund layering flow)")

    if graph_signals.get("is_smurfing"):
        reasons.append("Structuring detected (Multiple rapid small transactions between same accounts)")
        
    if graph_signals.get("is_cluster"):
        reasons.append("Part of an isolated, highly-active fraud cluster/clique")

    # 4. ML Anomaly
    score = risk_result.get("anomaly_score", 0)
    level = risk_result.get("anomaly_level", "LOW")
    if level != "LOW":
        reasons.append(f"AI Anomaly check returned {level} confidence score ({score:.2f})")

    # 5. Combined / Identity Intelligence
    if identity_signals and identity_signals.get("identity_count", 0) >= 3:
        reasons.append(f"Synthetic identity signal: {identity_signals['identity_count']} unique accounts linked to this device")

    if recent_scores and len([s for s in recent_scores if s > 50]) >= 2:
        reasons.append("Escalated risk due to repeated suspicious behavior in transaction history")

    if not reasons:
        reasons.append("No abnormal behavioral or relationship patterns detected")

    return reasons