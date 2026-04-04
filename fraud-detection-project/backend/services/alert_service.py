from backend.alerts.generator import create_alert
from backend.alerts.store import save_alert, get_all_alerts
from backend.db.repositories import save_alert_to_db, get_connection
from typing import Dict, Any, List
import json

def generate_and_store_alert(tx, decision, reasons) -> Dict[str, Any]:
    alert = create_alert(tx, decision, reasons)
    save_alert(alert) # In-memory for immediate speed
    
    # Persistent storage
    try:
        save_alert_to_db(alert)
    except Exception as e:
        print(f"Error persisting alert: {e}")
        
    return alert

def fetch_all_alerts() -> List[Dict[str, Any]]:
    # Combine in-memory with DB for robustness
    mem_alerts = get_all_alerts()
    if not mem_alerts:
        try:
            conn = get_connection()
            rows = conn.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 50").fetchall()
            conn.close()
            db_alerts = []
            for r in rows:
                db_alerts.append({
                    "alert_id": r["alert_id"],
                    "transaction_id": r["transaction_id"],
                    "sender_id": r["sender_id"],
                    "amount": r["amount"],
                    "action": r["action"],
                    "risk_score": r["risk_score"],
                    "reasons": json.loads(r["reasons"]),
                    "timestamp": r["timestamp"]
                })
            return db_alerts
        except Exception as e:
            print(f"Error fetching alerts from DB: {e}")
            return []
    return mem_alerts