import uuid
from datetime import datetime
from typing import Dict, Any

def create_alert(tx: Dict[str, Any], decision: Dict[str, Any], reasons: list) -> Dict[str, Any]:
    return {
        "alert_id": str(uuid.uuid4()),
        "transaction_id": tx.get("transaction_id", "unknown"),
        "sender_id": tx.get("sender_id"),
        "amount": tx.get("amount"),
        "action": decision.get("action"),
        "risk_score": decision.get("risk_score"),
        "reasons": reasons,
        "timestamp": datetime.utcnow().isoformat(),
    }