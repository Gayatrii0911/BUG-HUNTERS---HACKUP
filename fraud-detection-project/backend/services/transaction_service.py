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

    add_transaction(sender, receiver, amount)
    graph_result = generate_signals(sender, receiver, amount)
    graph_signals = graph_result.get("signals", {})

    behavior = get_behavior_analysis(tx)
    deviations = behavior["deviations"]
    device_info = behavior["device_info"]

    features = extract_features(tx, deviations, device_info)
    anomaly_score = score_transaction(features)

    risk_result = compute_risk_score(graph_signals, anomaly_score, deviations, device_info)
    decision = make_decision(risk_result["risk_score"], deviations, device_info)
    reasons = generate_explanation(deviations, device_info, graph_signals, anomaly_score, risk_result["components"])

    alert = generate_and_store_alert(tx, decision, reasons)
    update_user_profile(tx)

    try:
        save_transaction(tx, risk_result, decision)
        save_alert_to_db(alert)
        
        # ELITE GOLD: Adaptive Learning
        # Save features for retraining (assumed label 0 for now; in prod use confirmed feedback)
        save_training_sample(features, 0)
        
        global _tx_count
        _tx_count += 1
        if _tx_count >= RETRAIN_THRESHOLD:
            print(f"[ML] Retraining triggered at {_tx_count} transactions...")
            all_data = get_training_data()
            if all_data:
                retrain(all_data)
                _tx_count = 0 # reset
    except Exception as e:
        print(f"Post-processing error: {e}")

    return {
        "transaction_id": tx["transaction_id"],
        "action": decision["action"],
        "risk_score": risk_result["risk_score"],
        "risk_components": risk_result["components"],
        "reasons": reasons,
        "graph_signals": graph_signals,
        "anomaly_score": anomaly_score,
        "alert_id": alert["alert_id"],
    }