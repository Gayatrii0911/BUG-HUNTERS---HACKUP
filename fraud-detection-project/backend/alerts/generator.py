import uuid
from datetime import datetime
from typing import Dict, Any, List

def create_alert(tx: Dict[str, Any], decision: Dict[str, Any], reasons: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Extract primary pattern (highest severity)
    patterns = [r['message'] for r in reasons if r['type'] in ['graph', 'synergy', 'ml']]
    primary_pattern = patterns[0] if patterns else "Suspicious Pattern"

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