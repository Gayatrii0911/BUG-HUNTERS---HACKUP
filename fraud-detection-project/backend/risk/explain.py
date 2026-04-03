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
    Elite-level Categorized Explanation Engine.
    Returns a dictionary with:
    - 'reasons': List[Dict]
    - 'categories': {behavior: [], device: [], ml: [], graph: [], fraud_chain: []}
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
        msg = f"Transaction amount Rs {amount:,} exceeds 2x user average Rs {avg:,}"
        categories["behavior"].append({"message": msg, "type": "behavior"})
    elif deviations.get("amount_deviation", 0) > 2.5:
        msg = f"Transaction amount Rs {amount:,} is significantly higher than usual"
        categories["behavior"].append({"message": msg, "type": "behavior"})
    
    if deviations.get("time_deviation"):
        msg = "Transaction at an unusual hour for this user's profile"
        categories["behavior"].append({"message": msg, "type": "behavior"})
    
    if deviations.get("frequency_spike"):
        msg = "Transaction frequency increased significantly (possible smurfing)"
        categories["behavior"].append({"message": msg, "type": "behavior"})
        
    if deviations.get("self_transfer"):
        msg = "Suspicious self-transfer (Sender and Receiver are identical)"
        categories["behavior"].append({"message": msg, "type": "suspicious"})

    # 2. Device/Location Reasons (Including Identity Intelligence)
    if deviations.get("new_device"):
        msg = f"Login from new device (Device ID: {deviations.get('device_id', 'Unknown')})"
        categories["device"].append({"message": msg, "type": "device"})
    
    if deviations.get("new_location"):
        msg = f"Transaction from new location: {deviations.get('location', 'Unknown')}"
        categories["device"].append({"message": msg, "type": "device"})
    
    if device_info.get("impossible_travel"):
        msg = "Impossible travel detected (Dual location activity)"
        categories["device"].append({"message": msg, "type": "device"})
    
    if device_info.get("suspicious_channel"):
        msg = "Transaction routed through anonymizing network (VPN/Tor)"
        categories["device"].append({"message": msg, "type": "device"})

    if identity_signals and identity_signals.get("identity_count", 0) >= 3:
        msg = f"Synthetic identity signal: {identity_signals['identity_count']} unique accounts linked to this device"
        categories["device"].append({"message": msg, "type": "synergy"})

    # 3. ML Reasons
    score = risk_result.get("anomaly_score", 0)
    level = risk_result.get("anomaly_level", "LOW")
    if level != "LOW":
        msg = f"AI Anomaly check returned {level} confidence score ({score:.2f})"
        categories["ml"].append({"message": msg, "type": "ml"})

    # 4. Graph Reasons (Elite Detailed Signals)
    if graph_signals.get("has_cycle"):
        msg = "Cycle detected in transaction flow (Possible layering flow)"
        categories["graph"].append({"message": msg, "type": "graph"})
    
    if graph_signals.get("is_hub"):
        msg = f"Account flagged as 'Hub' (Connected to {graph_signals.get('connections', 0)} entities)"
        categories["graph"].append({"message": msg, "type": "graph"})

    if graph_signals.get("suspicious_chain"):
        msg = "Money laundering chain detected (Multi-hop layering flow)"
        categories["graph"].append({"message": msg, "type": "graph"})

    if graph_signals.get("is_smurfing"):
        msg = "Structuring detected (Multiple rapid small transactions)"
        categories["graph"].append({"message": msg, "type": "graph"})
        
    if graph_signals.get("is_cluster"):
        msg = "Part of an isolated, highly-active fraud cluster or clique"
        categories["graph"].append({"message": msg, "type": "graph"})

    # 5. Risk History
    if recent_scores and len([s for s in recent_scores if s >= 40]) >= 1:
        msg = "Recent historical risk escalation (repeated suspicious activity)"
        categories["behavior"].append({"message": msg, "type": "history"})

    # 6. Consistency Calibration: Ensure every contributing component has a reason
    scores = risk_result.get("components", {})
    if scores.get("behavior_risk", 0) > 0 and not categories["behavior"]:
        categories["behavior"].append({"message": "Non-standard behavioral patterns identified", "type": "behavior"})
    if scores.get("device_risk", 0) > 0 and not categories["device"]:
        categories["device"].append({"message": "Unusual hardware or connection metadata detected", "type": "device"})
    if scores.get("ml_risk", 0) > 0 and not categories["ml"]:
        categories["ml"].append({"message": "AI model identified subtle anomalous features", "type": "ml"})
    if scores.get("graph_risk", 0) > 0 and not categories["graph"]:
        categories["graph"].append({"message": "Anomalous fund flow relationships identified", "type": "graph"})

    # Flatten all reasons
    all_reasons = []
    for cat_list in categories.values():
        all_reasons.extend(cat_list)
        
    if not all_reasons:
        all_reasons.append({"message": "No abnormal behavioral or relationship patterns detected", "type": "baseline"})

    return {
        "reasons": all_reasons,
        "categories": categories
    }