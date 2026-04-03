def calculate_final_risk(graph_result: dict, ml_result: dict) -> float:
    score = 0.0

    # Graph signals
    if graph_result.get("cycle"):
        score += 40
    if graph_result.get("rapid_chain"):
        score += 20
    connections = graph_result.get("connections", 0)
    if connections > 5:
        score += 15
    elif connections > 2:
        score += 5
    score += graph_result.get("graph_risk", 0) * 0.3

    # ML + behavior signals
    score += ml_result.get("behavior_risk", 0) * 0.4
    score += ml_result.get("ml_risk", 0) * 0.3
    anomaly = ml_result.get("anomaly_score", 0)
    if anomaly > 0.8:
        score += 20
    elif anomaly > 0.5:
        score += 10

    # Device/location
    if not ml_result.get("device_known", True):
        score += 10
    if not ml_result.get("location_known", True):
        score += 5

    return round(min(score, 100), 2)