from typing import Dict, Any, List

def generate_explanation(
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    graph_signals: Dict[str, Any],
    risk_result: Dict[str, Any],
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

    # 2. Device/Location Reasons
    if deviations.get("new_device"):
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

    return {
        "reasons": all_reasons,
        "categories": categories
    }