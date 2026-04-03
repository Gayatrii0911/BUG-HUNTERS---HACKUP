from typing import List, Dict, Any

_alerts: List[Dict[str, Any]] = []

def save_alert(alert: Dict[str, Any]):
    _alerts.append(alert)

def get_all_alerts() -> List[Dict[str, Any]]:
    return list(reversed(_alerts))

def get_alerts_by_user(user_id: str) -> List[Dict[str, Any]]:
    return [a for a in _alerts if a.get("sender_id") == user_id]