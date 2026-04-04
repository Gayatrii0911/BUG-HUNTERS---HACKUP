import json
from datetime import datetime
from backend.db.database import get_connection
from typing import Dict, Any, List

def rebuild_graph_from_db():
    from backend.graph.graph_store import add_transaction, reset_graph
    try:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM transactions").fetchall()
        conn.close()
        reset_graph()
        for r in rows:
            # Re-inject historical data into the live NetworkX graph
            add_transaction(
                from_account=r["sender_id"],
                to_account=r["receiver_id"],
                amount=r["amount"],
                transaction_id=r["id"],
                decision=r["action"],
                risk_score=r["risk_score"],
                is_fraud=r["risk_score"] >= 70,
                is_blocked=r["action"] == "BLOCK"
            )
        print(f"SENTINEL-X GRAPH STORAGE RESTORED WITH {len(rows)} TRANSACTIONS FROM DB")
    except Exception as e:
        print(f"Error rebuilding graph: {e}")
def save_transaction(tx: Dict, risk_result: Dict, decision: Dict):
    try:
        conn = get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO transactions VALUES (?,?,?,?,?,?,?)
        """, (
            tx.get("transaction_id"),
            tx.get("sender_id"),
            tx.get("receiver_id"),
            tx.get("amount"),
            risk_result.get("risk_score"),
            decision.get("action"),
            datetime.utcnow().isoformat(),
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB save_transaction error: {e}")


def save_alert_to_db(alert: Dict):
    try:
        conn = get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO alerts VALUES (?,?,?,?,?,?,?,?)
        """, (
            alert["alert_id"],
            alert["transaction_id"],
            alert["sender_id"],
            alert["amount"],
            alert["action"],
            alert["risk_score"],
            json.dumps(alert["reasons"]),
            alert["timestamp"],
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB save_alert error: {e}")


def save_training_sample(features: List[float], label: int):
    try:
        conn = get_connection()
        conn.execute("""
            INSERT INTO ml_training_data (features, label, timestamp) VALUES (?,?,?)
        """, (json.dumps(features), label, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB save_training error: {e}")


def get_training_data() -> List[List[float]]:
    try:
        conn = get_connection()
        rows = conn.execute("SELECT features FROM ml_training_data").fetchall()
        conn.close()
        return [json.loads(r[0]) for r in rows]
    except Exception as e:
        print(f"DB get_training error: {e}")
        return []