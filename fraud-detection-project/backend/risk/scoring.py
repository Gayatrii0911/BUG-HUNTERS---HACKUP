from typing import Dict, Any

def compute_risk_score(
    graph_signals: Dict[str, Any],
    anomaly_score: float,
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    recent_scores: list = None
) -> Dict[str, Any]:
    """
    Elite-level scoring:
    1. Base weighted sum
    2. Combined Intelligence boost (Graph + ML)
    3. Risk Escalation (History)
    4. Categorization
    """
    graph_score = _graph_to_score(graph_signals)
    behavior_score = deviations.get("deviation_score", 0.0)
    device_score = device_info.get("device_risk", 0.0)

    # 1. Base Score
    combined = (
        graph_score * 0.35 +
        anomaly_score * 0.30 +
        behavior_score * 0.25 +
        device_score * 0.10
    )
    final_score = combined * 100

    # 2. Combined Intelligence (Coordinated Fraud)
    # If both graph and ML are high, boost the score
    if graph_score > 0.6 and anomaly_score > 0.6:
        final_score += 15
        print("[Scoring] Coordinated Fraud Boost applied")

    # 3. Risk Escalation (Adaptive History)
    if recent_scores:
        suspicious_count = len([s for s in recent_scores if s > 50])
        if suspicious_count >= 2:
            final_score += 10
            print(f"[Scoring] Risk Escalation applied ({suspicious_count} recent flags)")

    final_score = min(100.0, round(final_score, 1))

    # 4. Anomaly Interpretation
    if anomaly_score > 0.7:
        anomaly_level = "HIGH"
    elif anomaly_score > 0.4:
        anomaly_level = "MEDIUM"
    else:
        anomaly_level = "LOW"

    return {
        "risk_score": final_score,
        "risk_level": _get_risk_level(final_score),
        "anomaly_score": round(anomaly_score, 3),
        "anomaly_level": anomaly_level,
        "components": {
            "graph_risk": round(graph_score * 100, 1),
            "ml_risk": round(anomaly_score * 100, 1),
            "behavior_risk": round(behavior_score * 100, 1),
            "device_risk": round(device_score * 100, 1),
        }
    }

def _get_risk_level(score: float) -> str:
    if score >= 70: return "high"
    if score >= 40: return "medium"
    return "low"

def _graph_to_score(signals: Dict[str, Any]) -> float:
    # ... (rest stays the same or slightly improved)
    if not signals:
        return 0.0
    flags = [
        signals.get("has_cycle", False),
        signals.get("suspicious_connections", False),
        signals.get("rapid_transactions", False)
    ]
    raw = signals.get("score", 0)
    normalized = min(1.0, raw / 100.0) if isinstance(raw, (int, float)) else 0.0
    flag_score = sum(flags) / max(len(flags), 1)
    return round((normalized + flag_score) / 2, 3)
