from typing import Dict, Any

def compute_risk_score(
    graph_signals: Dict[str, Any],
    anomaly_score: float,
    deviations: Dict[str, Any],
    device_info: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Combines all signals into a final 0–100 risk score.
    Weights:
      - Graph signals  : 35%
      - ML anomaly     : 30%
      - Behavior       : 25%
      - Device         : 10%
    """
    graph_score = _graph_to_score(graph_signals)
    behavior_score = deviations.get("deviation_score", 0.0)
    device_score = device_info.get("device_risk", 0.0)

    combined = (
        graph_score * 0.35 +
        anomaly_score * 0.30 +
        behavior_score * 0.25 +
        device_score * 0.10
    )
    final = round(combined * 100, 1)

    return {
        "risk_score": final,
        "components": {
            "graph": round(graph_score * 100, 1),
            "anomaly_ml": round(anomaly_score * 100, 1),
            "behavior": round(behavior_score * 100, 1),
            "device": round(device_score * 100, 1),
        }
    }

def _graph_to_score(signals: Dict[str, Any]) -> float:
    """Convert Member 1's graph signals dict to a 0–1 score."""
    if not signals:
        return 0.0
    flags = []
    flags.append(signals.get("has_cycle", False))
    flags.append(signals.get("suspicious_connections", False))
    flags.append(signals.get("rapid_transactions", False))
    raw = signals.get("score", 0)
    normalized = min(1.0, raw / 100.0) if isinstance(raw, (int, float)) else 0.0
    flag_score = sum(flags) / max(len(flags), 1)
    return round((normalized + flag_score) / 2, 3)
