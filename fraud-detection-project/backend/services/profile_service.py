from backend.behavior.profile_store import get_profile, update_profile
from backend.behavior.profile_engine import compute_deviations
from backend.behavior.device_intelligence import analyze_device
from typing import Dict, Any

def get_behavior_analysis(tx: Dict[str, Any]) -> Dict[str, Any]:
    user_id = tx.get("sender_id", "unknown")
    deviations = compute_deviations(user_id, tx)
    device_info = analyze_device(tx)
    return {"deviations": deviations, "device_info": device_info}

def update_user_profile(tx: Dict[str, Any]):
    update_profile(tx.get("sender_id", "unknown"), tx)