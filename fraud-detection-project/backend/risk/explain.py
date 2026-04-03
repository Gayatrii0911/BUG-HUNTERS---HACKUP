from typing import Dict, Any, List

def generate_explanation(
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    graph_signals: Dict[str, Any],
    risk_result: Dict[str, Any],
<<<<<<< HEAD
    recent_scores: List[float] = None
) -> Dict[str, Any]:
    """
    Returns a dictionary with:
    - 'reasons': List[str]
    - 'reason_categories': {behavior: [], device: [], ml: [], graph: [], fraud_chain: []}
    """
    categories = {
        "behavior": [],
        "device": [],
        "ml": [],
        "graph": [],
        "fraud_chain": []
    }
    
    # 1. Behavioral Reasons
    if deviations.get("amount_exceeds_2x"):
        msg = f"Transaction amount ₹{deviations['current_amount']:,} exceeds 2x user average ₹{deviations['avg_amount']:,}"
        categories["behavior"].append(msg)
    elif deviations.get("amount_deviation", 0) > 2.5:
        categories["behavior"].append(f"Transaction amount is significantly higher than usual")
    
    if deviations.get("time_deviation"):
        categories["behavior"].append("Transaction at an unusual hour for this user")
    
    if deviations.get("frequency_spike"):
        categories["behavior"].append("Transaction frequency increased significantly")
=======
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
>>>>>>> e35f700abcf1402291ab08e82ea2fd2d2dbaa968

    # 2. Device/Location Reasons
    if deviations.get("new_device"):
<<<<<<< HEAD
        categories["device"].append(f"Login from new device (Device ID: {deviations.get('device_id', 'Unknown')})")
    
    if deviations.get("new_location"):
        categories["device"].append(f"Transaction from new location: {deviations.get('location', 'Unknown')}")
    
    if device_info.get("impossible_travel"):
        categories["device"].append("Impossible travel detected (Device active in multiple locations)")
    
    if device_info.get("suspicious_channel"):
        categories["device"].append("Transaction routed through anonymizing network (VPN/Tor)")

    # 3. ML Reasons
    score = risk_result.get("anomaly_score", 0)
    level = risk_result.get("anomaly_level", "LOW")
    if level != "LOW":
        categories["ml"].append(f"Anomaly score {score:.2f} classified as {level}")

    # 4. Graph Reasons
    if graph_signals.get("has_cycle"):
        categories["graph"].append("Cycle detected in transaction flow (Possible layering)")
    
    conn_count = graph_signals.get("connections", 0)
    if conn_count > 0:
        categories["graph"].append(f"Connected to {conn_count} related account(s) in transaction graph")

    # 5. Fraud Chain / History
    if recent_scores and len([s for s in recent_scores if s > 50]) >= 2:
        categories["fraud_chain"].append("Repeated suspicious activity detected in recent transactions")

    # Flatten all reasons
    all_reasons = []
    for cat_list in categories.values():
        all_reasons.extend(cat_list)
        
    if not all_reasons:
        all_reasons.append("Transaction characteristics align with historical behavioral profile")
=======
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
>>>>>>> e35f700abcf1402291ab08e82ea2fd2d2dbaa968

    return {
        "reasons": all_reasons,
        "categories": categories
    }