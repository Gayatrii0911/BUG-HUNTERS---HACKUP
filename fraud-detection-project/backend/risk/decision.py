def make_decision(risk_score: float) -> str:
    if risk_score >= 75:
        return "BLOCK"
    elif risk_score >= 45:
        return "MFA"
    else:
        return "APPROVE"