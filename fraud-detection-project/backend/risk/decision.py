from typing import Dict, Any

def make_decision(risk_score: float, deviations: Dict, device_info: Dict, risk_result: Dict) -> Dict[str, Any]:
    """
    Elite-level decisioning:
    - Threshold-based actions
    - Fraud chain markers (ATO detection)
    """
    anomaly_score = risk_result.get("anomaly_score", 0.0)
    
    if risk_score >= 70:
        action = "BLOCK"
        color = "red"
    elif risk_score >= 40:
        action = "MFA"
        color = "amber"
    else:
        action = "APPROVE"
        color = "green"

    # Fraud Chain Detection logic:
    # (new device OR new location) AND anomaly_score > 0.5
    is_new_access = deviations.get("new_device", False) or deviations.get("new_location", False)
    fraud_chain = is_new_access and anomaly_score > 0.5

    # Force BLOCK if fraud chain is detected
    if fraud_chain:
        action = "BLOCK"
        color = "red"

    return {
        "action": action,
        "color": color,
        "risk_score": risk_score,
        "fraud_chain_detected": fraud_chain,
        "is_pre_transaction_check": True
    }
