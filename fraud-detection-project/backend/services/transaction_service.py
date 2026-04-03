import time
import uuid
from backend.graph.builder import add_transaction
from backend.graph.algorithms import generate_signals
from backend.services.profile_service import get_behavior_analysis, update_user_profile
from backend.ml.features import extract_features
from backend.ml.anomaly import score_transaction, retrain
from backend.risk.scoring import compute_risk_score
from backend.risk.decision import make_decision
from backend.risk.explain import generate_explanation
from backend.services.alert_service import generate_and_store_alert
from backend.db.repositories import save_transaction, save_alert_to_db, save_training_sample, get_training_data

_tx_count = 0
RETRAIN_THRESHOLD = 20

def process_transaction(tx: dict) -> dict:
    if not tx.get("transaction_id"):
        tx["transaction_id"] = str(uuid.uuid4())
    if not tx.get("timestamp"):
        tx["timestamp"] = str(time.time())

    sender = tx.get("sender_id", "unknown")
    receiver = tx.get("receiver_id", "unknown")
    amount = tx.get("amount", 0)

    # ... (Graph / Behavior / ML parts)
    add_transaction(sender, receiver, amount)
    graph_result = generate_signals(sender, receiver, amount)
    graph_signals = graph_result.get("signals", {})

    from backend.behavior.profile_store import get_profile # for history
    profile = get_profile(sender)
    behavior = get_behavior_analysis(tx)
    deviations = behavior["deviations"]
    device_info = behavior["device_info"]

    features = extract_features(tx, deviations, device_info)
    anomaly_score = score_transaction(features)

    # 1. Compute Scored Result (Categorized & Escalated)
    risk_result = compute_risk_score(
        graph_signals, 
        anomaly_score, 
        deviations, 
        device_info, 
        profile["recent_risk_scores"]
    )
    
    # 2. Decision Logic (Chain Detection)
    decision = make_decision(
        risk_result["risk_score"], 
        deviations, 
        device_info, 
        risk_result["anomaly_level"]
    )
    
    # 3. Explainability (Human-Readable)
    reasons = generate_explanation(
        deviations, 
        device_info, 
        graph_signals, 
        risk_result, 
        profile["recent_risk_scores"]
    )

    alert = generate_and_store_alert(tx, decision, reasons)
    
    # Update behavioral profile (including risk history)
    update_user_profile(tx)
    profile["recent_risk_scores"].append(risk_result["risk_score"])
    if len(profile["recent_risk_scores"]) > 5:
        profile["recent_risk_scores"].pop(0)

    try:
        save_transaction(tx, risk_result, decision)
        save_alert_to_db(alert)
        save_training_sample(features, 0)
        
        global _tx_count
        _tx_count += 1
        if _tx_count >= RETRAIN_THRESHOLD:
            print(f"[ML] Retraining triggered at {_tx_count} transactions...")
            all_data = get_training_data()
            if all_data:
                retrain(all_data)
                _tx_count = 0
    except Exception as e:
        print(f"Post-processing error: {e}")

    # ELITE RESPONSE STRUCTURE
    return {
        "transaction_id": tx["transaction_id"],
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"],
        "decision": decision["action"],
        "reasons": reasons,
        "score_breakdown": risk_result["components"],
        "anomaly_score": risk_result["anomaly_score"],
        "anomaly_level": risk_result["anomaly_level"],
        "fraud_chain_detected": decision.get("fraud_chain_detected", False),
        "is_pre_transaction_check": True,
        "alert": risk_result["risk_score"] >= 40,
        "alert_id": alert["alert_id"]
    }