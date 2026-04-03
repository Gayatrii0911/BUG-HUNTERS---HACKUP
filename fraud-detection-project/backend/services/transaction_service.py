import time
import uuid
from backend.graph.builder import add_transaction, get_graph
from backend.graph.algorithms import generate_signals
from backend.services.profile_service import get_behavior_analysis, update_user_profile
from backend.ml.features import extract_features
from backend.ml.anomaly import score_transaction, retrain
from backend.risk.scoring import compute_risk_score
from backend.risk.decision import make_decision
from backend.risk.explain import generate_explanation
from backend.services.alert_service import generate_and_store_alert
from backend.db.repositories import save_transaction, save_alert_to_db, save_training_sample, get_training_data
from backend.behavior.profile_store import get_profile, get_device_users

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

    # 1. Graph Intelligence (Real-time update & Analysis)
    add_transaction(sender, receiver, amount)
    graph_res = generate_signals(sender, receiver, amount)
    graph_signals = graph_res.get("signals", {})

    # 2. Behavioral / Device Intelligence
    profile = get_profile(sender)
    behavior = get_behavior_analysis(tx)
    deviations = behavior["deviations"]
    device_info = behavior["device_info"]

    # 3. Synthetic Identity Detection (Cross-User hardware)
    device_id = tx.get("device_id", "unknown")
    associated_users = get_device_users(device_id) if device_id != "unknown" else []
    identity_signals = {
        "shared_hardware_users": associated_users,
        "identity_count": len(associated_users)
    }

    # 4. ML Anomly Scoring
    features = extract_features(tx, deviations, device_info)
    anomaly_score = score_transaction(features)

    # 5. Elite Fusion Scoring (Coordinated + History + Identity)
    risk_result = compute_risk_score(
        graph_signals, 
        anomaly_score, 
        deviations, 
        device_info, 
        profile["recent_risk_scores"],
        identity_signals
    )
    
    # 6. Decision & Explanation
    decision = make_decision(
        risk_result["risk_score"], 
        deviations, 
        device_info, 
        risk_result
    )
    
    # Fraud Chain Boost (if detected)
    final_risk_score = risk_result["risk_score"]
    if decision.get("fraud_chain_detected"):
        final_risk_score = min(100.0, final_risk_score + 20.0)
        risk_result["risk_score"] = final_risk_score
        from backend.risk.scoring import _get_risk_level
        risk_result["risk_level"] = _get_risk_level(final_risk_score)
        decision = make_decision(final_risk_score, deviations, device_info, risk_result)

    explanation_result = generate_explanation(
        deviations, 
        device_info, 
        graph_signals, 
        risk_result, 
        profile["recent_risk_scores"],
        identity_signals
    )
    
    reasons = explanation_result["reasons"]
    reason_categories = explanation_result["categories"]

    # If fraud chain detected, add specifically to categories
    if decision.get("fraud_chain_detected"):
        chain_msg = "Suspicious login followed by anomalous transaction (possible account takeover)"
        if chain_msg not in reason_categories["fraud_chain"]:
            reason_categories["fraud_chain"].append(chain_msg)
            reasons.append(chain_msg)

    alert = generate_and_store_alert(tx, decision, reasons)
    
    # 7. Persistence & Lifecycle
    update_user_profile(tx)
    profile["recent_risk_scores"].append(final_risk_score)
    if len(profile["recent_risk_scores"]) > 5:
        profile["recent_risk_scores"].pop(0)

    try:
        save_transaction(tx, risk_result, decision)
        save_training_sample(features, 0)
        
        global _tx_count
        _tx_count += 1
        if _tx_count >= RETRAIN_THRESHOLD:
            all_data = get_training_data()
            if all_data:
                retrain(all_data)
                _tx_count = 0
    except Exception as e:
        print(f"Post-processing error: {e}")

    # ELITE RESPONSE (Full Section 9 Compatibility)
    return {
        "transaction_id": tx["transaction_id"],
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"],
        "decision": decision["action"],
        "reasons": reasons,
        "reason_categories": reason_categories,
        "score_breakdown": risk_result["components"],
        "anomaly_score": risk_result["anomaly_score"],
        "anomaly_level": risk_result["anomaly_level"],
        "confidence": risk_result["confidence"],
        "fraud_chain_detected": decision.get("fraud_chain_detected", False),
        "is_pre_transaction_check": True,
        "alert": risk_result["risk_score"] >= 40,
    }