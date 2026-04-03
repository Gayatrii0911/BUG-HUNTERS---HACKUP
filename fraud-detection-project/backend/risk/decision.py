from typing import Dict, Any

def make_decision(risk_score: float, deviations: Dict, device_info: Dict, anomaly_level: str) -> Dict[str, Any]:
    """
    Elite-level decisioning:
    - Threshold-based actions
    - Overrides for extreme threats
    - Fraud chain markers
    """
    if risk_score >= 70:
        action = "BLOCK"
        color = "red"
    elif risk_score >= 40:
        action = "MFA"
        color = "amber"
    else:
        action = "APPROVE"
        color = "green"

    # Fraud Chain Detection: (New Device/Location) + HIGH Anomaly
    is_ato_signal = deviations.get("new_device") or device_info.get("impossible_travel")
    fraud_chain = is_ato_signal and anomaly_level == "HIGH"

    # Override: Force BLOCK on fraud chains
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
