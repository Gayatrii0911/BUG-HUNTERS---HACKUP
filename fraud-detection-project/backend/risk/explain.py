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
    amount = deviations.get("amount", deviations.get("current_amount", 0))
    avg = deviations.get("avg_amount", 0)
    if deviations.get("amount_exceeds_2x"):
        categories["behavior"].append(f"Transaction amount Rs {amount:,} exceeds 2x user average Rs {avg:,}")
    elif deviations.get("amount_deviation", 0) > 2.5:
        categories["behavior"].append(f"Transaction amount Rs {amount:,} is significantly higher than usual")
    
    if deviations.get("time_deviation"):
        categories["behavior"].append("Transaction at an unusual hour for this user's profile")
    
    if deviations.get("frequency_spike"):
        categories["behavior"].append("Transaction frequency increased significantly (possible smurfing)")

    # 2. Device/Location Reasons (Including Identity Intelligence)
    if deviations.get("new_device"):
        categories["device"].append(f"Login from new device (Device ID: {deviations.get('device_id', 'Unknown')})")
    
    if deviations.get("new_location"):
        categories["device"].append(f"Transaction from new location: {deviations.get('location', 'Unknown')}")
    
    if device_info.get("impossible_travel"):
        categories["device"].append("Impossible travel detected (Dual location activity)")
    
    if device_info.get("suspicious_channel"):
        categories["device"].append("Transaction routed through anonymizing network (VPN/Tor)")

    if identity_signals and identity_signals.get("identity_count", 0) >= 3:
        categories["device"].append(f"Synthetic identity signal: {identity_signals['identity_count']} unique accounts linked to this device")

    # 3. ML Reasons
    score = risk_result.get("anomaly_score", 0)
    level = risk_result.get("anomaly_level", "LOW")
    if level != "LOW":
        categories["ml"].append(f"AI Anomaly check returned {level} confidence score ({score:.2f})")

    # 4. Graph Reasons (Elite Detailed Signals)
    if graph_signals.get("has_cycle"):
        categories["graph"].append("Cycle detected in transaction flow (Possible layering flow)")
    
    if graph_signals.get("is_hub"):
        categories["graph"].append(f"Account flagged as 'Hub' (Connected to {graph_signals.get('connections', 0)} entities)")

    if graph_signals.get("suspicious_chain"):
        categories["graph"].append("Money laundering chain detected (Multi-hop layering flow)")

    if graph_signals.get("is_smurfing"):
        categories["graph"].append("Structuring detected (Multiple rapid small transactions)")
        
    if graph_signals.get("is_cluster"):
        categories["graph"].append("Part of an isolated, highly-active fraud cluster or clique")

    # 5. Fraud Chain / History
    if recent_scores and len([s for s in recent_scores if s > 50]) >= 2:
        categories["fraud_chain"].append("Repeated suspicious activity detected in recent transactions")

    # Flatten all reasons
    all_reasons = []
    for cat_list in categories.values():
        all_reasons.extend(cat_list)
        
    if not all_reasons:
        all_reasons.append("No abnormal behavioral or relationship patterns detected")

    return {
        "reasons": all_reasons,
        "categories": categories
    }