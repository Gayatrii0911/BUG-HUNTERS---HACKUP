from backend.alerts.generator import create_alert
from backend.alerts.store import save_alert, get_all_alerts
from typing import Dict, Any, List

def generate_and_store_alert(tx, decision, reasons) -> Dict[str, Any]:
    alert = create_alert(tx, decision, reasons)
    save_alert(alert)
    return alert

def fetch_all_alerts() -> List[Dict[str, Any]]:
    return get_all_alerts()