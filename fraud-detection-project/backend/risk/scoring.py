from typing import Dict, Any

def compute_risk_score(
    graph_signals: Dict[str, Any],
    anomaly_score: float,
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    recent_scores: list = None,
    identity_signals: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Elite-level scoring:
    1. Base weighted sum
    2. Combined Intelligence boost (Graph + ML)
    3. Synthetic Identity penalty (Shared hardware)
    4. Risk Escalation (History)
    """
    graph_score = _graph_to_score(graph_signals)
    behavior_score = deviations.get("deviation_score", 0.0)
    device_score = device_info.get("device_risk", 0.0)

    # 1. Base Score (40% Graph, 30% ML, 20% Behavior, 10% Device)
    combined = (
        graph_score * 0.40 +
        anomaly_score * 0.30 +
        behavior_score * 0.20 +
        device_score * 0.10
    )
    final_score = combined * 100

    # 2. Combined Intelligence Boost (Coordinated Fraud)
    if graph_score > 0.6 and anomaly_score > 0.6:
        final_score += 15
        
    # 3. Synthetic Identity Check (Multi-user hardware fingerprint)
    if identity_signals and identity_signals.get("identity_count", 0) >= 3:
        # High-risk signal: 3+ unique accounts on same literal device
        final_score += 20
        print(f"[Scoring] Synthetic Identity Penalty applied ({identity_signals['identity_count']} users)")

    # 4. Risk Escalation (Adaptive History)
    if recent_scores:
        suspicious_count = len([s for s in recent_scores if s > 50])
        if suspicious_count >= 2:
            final_score += 10

    final_score = min(100.0, round(final_score, 1))

    # Categorization
    if anomaly_score > 0.7: anomaly_level = "HIGH"
    elif anomaly_score > 0.4: anomaly_level = "MEDIUM"
    else: anomaly_level = "LOW"

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
    if not signals: return 0.0
    # Factors: Cycle, Hub, Velocity/Chain, Structuring, Cluster
    flags = [
        signals.get("has_cycle", False),
        signals.get("is_hub", False),
        signals.get("suspicious_chain", False),
        signals.get("is_smurfing", False),
        signals.get("is_cluster", False)
    ]
    raw = signals.get("score", 0)
    normalized = min(1.0, raw / 100.0) if isinstance(raw, (int, float)) else 0.0
    flag_score = sum(flags) / max(len(flags), 1)
    return round((normalized + flag_score) / 2, 3)
