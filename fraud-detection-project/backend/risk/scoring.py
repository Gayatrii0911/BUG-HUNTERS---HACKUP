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
    Elite Fusion Scoring:
    - Weights: Graph (30%), ML (25%), Behavior (25%), Device (20%)
    - Confidence score & Minimum Risk Floor
    - Synthetic Identity penalty (+20 for shared hardware)
    - Coordinated Fraud boost (+15 for Graph + ML agreement)
    """
    # 1. Normalize Graph Risk
    graph_score = _graph_to_score(graph_signals)
    behavior_score = deviations.get("deviation_score", 0.0)
    device_score = device_info.get("device_risk", 0.0)

    # 2. Base Score calculation with refined weights
    weighted_sum = (
        graph_score * 0.30 +
        anomaly_score * 0.35 +
        behavior_score * 0.25 +
        device_score * 0.10
    )
    
    final_score = weighted_sum * 100

    # 3. Combined Intelligence Boost (Coordinated Fraud)
    if graph_score >= 0.5 and anomaly_score >= 0.4:
        final_score += 30
        
    # 4. Synthetic Identity Check
    if identity_signals and identity_signals.get("identity_count", 0) >= 3:
        final_score += 20

    # 5. Risk Escalation (Adaptive History)
    if recent_scores:
        suspicious_count = len([s for s in recent_scores if s >= 40])
        if suspicious_count >= 1:
            final_score += 15

    # 6. Anomaly Level & Minimum Risk Floor
    if anomaly_score > 0.6:
        anomaly_level = "HIGH"
        final_score = max(final_score, 80.0)
    elif anomaly_score > 0.35:
        anomaly_level = "MEDIUM"
        final_score = max(final_score, 55.0)
    else:
        anomaly_level = "LOW"

    # 7. Fraud Chain Pre-calculation for Confidence
    is_new_access = deviations.get("new_device", False) or deviations.get("new_location", False)
    fraud_chain = is_new_access and anomaly_score > 0.5

    # 8. Confidence Calculation
    confidence = _calculate_confidence(graph_score, anomaly_score, behavior_score, device_score, fraud_chain)

    final_score = min(100.0, round(final_score, 1))

    return {
        "risk_score": final_score,
        "risk_level": _get_risk_level(final_score),
        "anomaly_score": round(anomaly_score, 3),
        "anomaly_level": anomaly_level,
        "confidence": round(confidence, 2),
        "fraud_chain_pre_check": fraud_chain,
        "components": {
            "graph_risk": round(graph_score * 100, 1),
            "ml_risk": round(anomaly_score * 100, 1),
            "behavior_risk": round(behavior_score * 100, 1),
            "device_risk": round(device_score * 100, 1),
        }
    }

def _calculate_confidence(g: float, a: float, b: float, d: float, f: bool) -> float:
    """
    Tiered Confidence logic:
    - 1 signal: 0.3
    - 2 signals: 0.6
    - 3+ signals: 0.85-0.95
    """
    signals_triggered = 0
    if g > 0: signals_triggered += 1
    if a > 0.3: signals_triggered += 1 # ml threshold
    if b > 0: signals_triggered += 1
    if d > 0: signals_triggered += 1
    if f: signals_triggered += 1
    
    if signals_triggered == 0: return 0.1
    if signals_triggered == 1: return 0.3
    if signals_triggered == 2: return 0.6
    if signals_triggered == 3: return 0.85
    if signals_triggered == 4: return 0.90
    return 0.95 # 5 signals

def _get_risk_level(score: float) -> str:
    if score >= 70: return "high"
    if score >= 40: return "medium"
    return "low"

def _graph_to_score(signals: Dict[str, Any]) -> float:
    if not signals: return 0.0
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
    
    connections = signals.get("connections", 0)
    if connections > 0:
        normalized = max(normalized, min(1.0, connections / 10.0))
        
    return round((normalized + flag_score) / 2, 3)
