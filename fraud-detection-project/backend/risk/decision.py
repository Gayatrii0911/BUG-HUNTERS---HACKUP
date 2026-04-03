from typing import Dict, Any

def make_decision(risk_score: float, deviations: Dict, device_info: Dict) -> Dict[str, Any]:
    """
    APPROVE  : risk < 40
    MFA      : 40 <= risk < 70
    BLOCK    : risk >= 70
    """
    if risk_score >= 70:
        action = "BLOCK"
        reason = "High fraud risk detected"
        color = "red"
    elif risk_score >= 40:
        action = "MFA"
        reason = "Elevated risk — additional verification required"
        color = "amber"
    else:
        action = "APPROVE"
        reason = "Transaction appears legitimate"
        color = "green"

    # Override to BLOCK on extreme device signals
    if device_info.get("impossible_travel") and device_info.get("device_user_mismatch"):
        action = "BLOCK"
        reason = "Device conflict + impossible travel detected"
        color = "red"

    return {
        "action": action,
        "reason": reason,
        "color": color,
        "risk_score": risk_score,
    }
