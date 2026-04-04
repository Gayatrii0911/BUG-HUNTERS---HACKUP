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

def get_fraud_type(reasons_text):
    if not reasons_text: return 'anomaly'
    rs = str(reasons_text).lower()
    if 'cycle' in rs or 'hub' in rs or 'chain' in rs or 'smurf' in rs:
        return 'money_laundering'
    if 'takeover' in rs or 'identity' in rs or 'device' in rs or 'location' in rs:
        return 'account_takeover'
    if 'synthetic' in rs or 'fingerprint' in rs:
        return 'synthetic_identity'
    return 'anomaly'

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
                reasons = json.loads(r["reasons"])
                ftype = get_fraud_type(r["reasons"])
                db_alerts.append({
                    "alert_id": r["alert_id"],
                    "transaction_id": r["transaction_id"],
                    "sender_id": r["sender_id"],
                    "amount": r["amount"],
                    "action": r["action"],
                    "risk_score": r["risk_score"],
                    "reasons": reasons,
                    "fraud_type": ftype,
                    "timestamp": r["timestamp"]
                })
            return db_alerts
        except Exception as e:
            print(f"Error fetching alerts from DB: {e}")
            return []
    
    # Also attach fraud_type to mem_alerts if they lack it
    for ma in mem_alerts:
        if 'fraud_type' not in ma:
            ma['fraud_type'] = get_fraud_type(str(ma.get('reasons', '')))
    return mem_alerts