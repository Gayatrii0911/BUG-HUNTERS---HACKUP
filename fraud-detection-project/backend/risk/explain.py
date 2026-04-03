from typing import Dict, Any, List

def generate_explanation(
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    graph_signals: Dict[str, Any],
    risk_result: Dict[str, Any],
    recent_scores: List[float] = None,
    identity_signals: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Elite-level Categorized Explanation Engine (Aligned with Team Contract).
    Returns both a flat list and a categorized mapping.
    """
    reasons = []
    categories = {
        "behavior": [],
        "device": [],
        "ml": [],
        "graph": [],
        "fraud_chain": []
    }
    
    # 1. Behavioral (Specific)
    amount = deviations.get("amount", 0)
    avg = deviations.get("avg_amount", 0)
    if deviations.get("amount_deviation", 0) > 2.5:
        msg = f"Amount {amount:,} significantly exceeds user average {avg:,}"
        reasons.append(msg)
        categories["behavior"].append(msg)
    
    if deviations.get("time_deviation"):
        msg = "Transaction at unusual hour for this historic profile"
        reasons.append(msg)
        categories["behavior"].append(msg)

    # 2. Device Intelligence
    if deviations.get("new_device"):
        msg = f"First-time usage of hardware fingerprint {deviations.get('device_id', 'Unlisted')}"
        reasons.append(msg)
        categories["device"].append(msg)

    if device_info.get("impossible_travel"):
        msg = "Impossible travel detected (Dual location activity)"
        reasons.append(msg)
        categories["device"].append(msg)
    
    if device_info.get("suspicious_channel"):
        msg = "Transaction routed through anonymizing network (VPN/Tor)"
        reasons.append(msg)
        categories["device"].append(msg)

    # 3. Graph Intelligence
    if graph_signals.get("has_cycle"):
        msg = "Circular money movement detected (Layering/Laundering)"
        reasons.append(msg)
        categories["graph"].append(msg)
    
    if graph_signals.get("is_hub"):
        msg = "Account flagged as transaction hub (suspicious fan-out)"
        reasons.append(msg)
        categories["graph"].append(msg)

    if graph_signals.get("suspicious_chain"):
        msg = "Involved in a multi-hop suspicious layering path"
        reasons.append(msg)
        categories["graph"].append(msg)

    if graph_signals.get("is_smurfing"):
        msg = "Structuring detected (Multiple rapid small transactions)"
        reasons.append(msg)
        categories["graph"].append(msg)

    # 4. ML Anomaly
    score = risk_result.get("anomaly_score", 0)
    level = risk_result.get("anomaly_level", "LOW")
    if level != "LOW":
        msg = f"AI Anomaly check returned {level} confidence score ({score:.2f})"
        reasons.append(msg)
        categories["ml"].append(msg)

    # 5. Fraud Chain / Synergy / History
    if identity_signals and identity_signals.get("identity_count", 0) >= 3:
        msg = f"Synthetic identity signal: {identity_signals['identity_count']} unique accounts on device"
        reasons.append(msg)
        categories["fraud_chain"].append(msg)

    if recent_scores and len([s for s in recent_scores if s > 50]) >= 2:
        msg = "Repeated suspicious behavioral history detected"
        reasons.append(msg)
        categories["fraud_chain"].append(msg)

    # Coordinated Synergy
    if risk_result.get("components", {}).get("graph_risk", 0) > 60 and risk_result.get("components", {}).get("ml_risk", 0) > 60:
        msg = "Network Synergy: Coordinated graph and AI triggers detected"
        reasons.append(msg)
        categories["fraud_chain"].append(msg)

    if not reasons:
        reasons.append("No abnormal patterns detected")

    return {
        "reasons": reasons,
        "reason_categories": categories
    }