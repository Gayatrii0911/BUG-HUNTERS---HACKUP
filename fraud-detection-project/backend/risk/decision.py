from typing import Dict, Any

def make_decision(risk_score: float, deviations: Dict, device_info: Dict, risk_result: Dict) -> Dict[str, Any]:
    """
    Elite-level decisioning:
    - Threshold-based actions
    - AI Calibration: MFA for 3x avg + 0.4 anomaly
    - Fraud type tagging for demo impact
    """
    anomaly_score = risk_result.get("anomaly_score", 0.0)
    anomaly_level = risk_result.get("anomaly_level", "LOW")
    graph_risk = risk_result.get("components", {}).get("graph_risk", 0.0)
    
    # 1. Base Action based on Risk Score
    if risk_score >= 70:
        action = "BLOCK"
        color = "red"
    elif risk_score >= 40:
        action = "MFA"
        color = "amber"
    else:
        action = "APPROVE"
        color = "green"

    # 2. MFA Calibration Rule: 3x Mean + Medium Anomaly
    avg = deviations.get("avg_amount", 0)
    amount = deviations.get("current_amount", 0)
    if avg > 0 and amount > (3 * avg) and anomaly_score >= 0.4:
        if action == "APPROVE":
            action = "MFA"
            color = "amber"

    # 3. Fraud Chain Detection (ATO detection)
    is_new_access = deviations.get("new_device", False) or deviations.get("new_location", False)
    fraud_chain = is_new_access and anomaly_score >= 0.3
    
    if fraud_chain:
        action = "BLOCK"
        color = "red"

    # 4. Critical Fraud High-Impact Flag
    critical_fraud = False
    if fraud_chain and (anomaly_level in ["HIGH", "MEDIUM"]) and graph_risk > 20:
        critical_fraud = True
        action = "BLOCK"
        color = "red"

    # 5. Demo Tagging (fraud_type)
    fraud_type = "normal"
    if critical_fraud:
        fraud_type = "account_takeover"
    elif fraud_chain:
        fraud_type = "anomaly"
    elif graph_risk > 30:
        fraud_type = "money_laundering"
    elif risk_score > 50 and deviations.get("identity_count", 0) >= 3:
        fraud_type = "synthetic_identity"
    elif risk_score > 30:
        fraud_type = "anomaly"

    return {
        "action": action,
        "color": color,
        "risk_score": risk_score,
        "fraud_chain_detected": fraud_chain,
        "critical_fraud": critical_fraud,
        "fraud_type": fraud_type,
        "is_pre_transaction_check": True
    }
