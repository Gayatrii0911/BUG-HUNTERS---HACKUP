from typing import Dict, Any

def compute_risk_score(
    graph_signals: Dict[str, Any],
    anomaly_score: float,
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
    recent_scores: list = None
) -> Dict[str, Any]:
    """
    Refined Elite scoring:
    - Weights: Graph (30%), ML (25%), Behavior (25%), Device (20%)
    - Confidence score
    - Minimum Risk Floor
    """
    graph_score = _graph_to_score(graph_signals)
    behavior_score = deviations.get("deviation_score", 0.0)
    device_score = device_info.get("device_risk", 0.0)

    # 1. Base Score calculation with new weights
    # Normalize components: Graph(0-1), ML(0-1), Behavior(0-1), Device(0-1)
    weighted_sum = (
        graph_score * 0.30 +
        anomaly_score * 0.25 +
        behavior_score * 0.25 +
        device_score * 0.20
    )
    
    final_score = weighted_sum * 100

    # 2. Minimum Risk Floor
    # Anomaly Level thresholds
    if anomaly_score > 0.7:
        anomaly_level = "HIGH"
        final_score = max(final_score, 50.0)
    elif anomaly_score > 0.4:
        anomaly_level = "MEDIUM"
        final_score = max(final_score, 25.0)
    else:
        anomaly_level = "LOW"

    # 3. Confidence Calculation
    confidence = _calculate_confidence(graph_score, anomaly_score, behavior_score, device_score)

    # 4. Result Assembly
    final_score = min(100.0, round(final_score, 1))

    return {
        "risk_score": final_score,
        "risk_level": _get_risk_level(final_score),
        "anomaly_score": round(anomaly_score, 3),
        "anomaly_level": anomaly_level,
        "confidence": round(confidence, 2),
        "components": {
            "graph_risk": round(graph_score * 100, 1),
            "ml_risk": round(anomaly_score * 100, 1),
            "behavior_risk": round(behavior_score * 100, 1),
            "device_risk": round(device_score * 100, 1),
        }
    }

def _calculate_confidence(g: float, a: float, b: float, d: float) -> float:
    """
    High confidence if multiple high-risk signals agree.
    Low confidence if only one weak signal is present.
    """
    signals = [g, a, b, d]
    strong_signals = [s for s in signals if s > 0.6]
    weak_signals = [s for s in signals if 0.2 < s <= 0.6]
    
    if len(strong_signals) >= 2:
        return 0.85 + (0.05 * len(strong_signals))
    if len(strong_signals) == 1 and len(weak_signals) >= 1:
        return 0.70
    if len(strong_signals) == 1:
        return 0.50
    return 0.30

def _get_risk_level(score: float) -> str:
    if score >= 70: return "high"
    if score >= 40: return "medium"
    return "low"

def _graph_to_score(signals: Dict[str, Any]) -> float:
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
    
    # Check for direct multi-connection signal from Member 1
    connections = signals.get("connections", 0)
    if connections > 0:
        normalized = max(normalized, min(1.0, connections / 10.0))
        
    return round((normalized + flag_score) / 2, 3)
