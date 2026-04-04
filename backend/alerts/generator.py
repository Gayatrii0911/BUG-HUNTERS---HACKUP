import uuid
from datetime import datetime
from typing import Dict, Any, List

def create_alert(tx: Dict[str, Any], decision: Dict[str, Any], reasons: List[str]) -> Dict[str, Any]:
    """
    Finalized Alert Generator.
    Hardened to handle flat reason strings for Elite Dashboard compatibility.
    """
    # Extract primary pattern from reasons (heuristically)
    # If reasons contains Graph keywords, mark as Graph pattern, etc.
    primary_pattern = "Suspicious Behavioral Drift"
    if reasons:
        for r in reasons:
            if "Cycle" in r or "Hub" in r or "Chain" in r or "Smurfing" in r:
                primary_pattern = "Graph/Network Relationship Alert"
                break
            if "AI" in r or "Anomaly" in r:
                primary_pattern = "AI Model Anomaly Detection"
                break

    return {
        "alert_id": f"ALT-{str(uuid.uuid4())[:8].upper()}",
        "transaction_id": tx.get("transaction_id", "unsigned"),
        "sender_id": tx.get("sender_id", "unknown"),
        "receiver_id": tx.get("receiver_id", "unknown"),
        "amount": tx.get("amount", 0.0),
        "pattern": primary_pattern,
        "action": decision.get("action", "REVIEW"),
        "risk_score": decision.get("risk_score", 0.0),
        "reasons": reasons,
        "is_investigated": False,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }