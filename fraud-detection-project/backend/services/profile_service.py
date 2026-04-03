from backend.behavior.profile_store import get_profile, update_profile
from backend.behavior.behavioral_analyzer import analyze_behavior
from typing import Dict, Any

def get_behavior_analysis(tx: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrates user-centric and device-centric behavior analysis.
    Unified via behavioral_analyzer for reduced duplication.
    """
    return analyze_behavior(tx)

def update_user_profile(tx: Dict[str, Any]):
    update_profile(tx.get("sender_id", "unknown"), tx)