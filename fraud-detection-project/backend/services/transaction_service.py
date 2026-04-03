from backend.graph.algorithms import process_graph
from backend.risk.scoring import calculate_final_risk
from backend.risk.decision import make_decision
from backend.risk.explain import generate_reasons


def process_transaction(tx):
    # Step 1: Graph analysis (Member 1)
    try:
        graph_result = process_graph(tx)
    except Exception:
        graph_result = {
            "cycle": False,
            "connections": 0,
            "rapid_chain": False,
            "graph_risk": 0,
            "related_accounts": []
        }

    # Step 2: ML + Behavior (Member 2) — mocked until Member 2 is ready
    ml_result = {
        "behavior_risk": 10,
        "anomaly_score": 0.3,
        "ml_risk": 15,
        "device_known": True,
        "location_known": True,
        "behavior_reasons": []
    }

    # Step 3: Combined risk score
    risk_score = calculate_final_risk(graph_result, ml_result)

    # Step 4: Decision
    decision = make_decision(risk_score)

    # Step 5: Reasons
    reasons = generate_reasons(graph_result, ml_result, risk_score)

    # Step 6: Alert flag
    alert = decision in ["BLOCK", "MFA"]

    # Step 7: Risk level label
    if risk_score >= 75:
        risk_level = "high"
    elif risk_score >= 45:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "decision": decision,
        "reasons": reasons,
        "alert": alert
    }