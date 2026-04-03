from fastapi import APIRouter, HTTPException
from backend.behavior.profile_store import get_profile, get_device_users
from backend.graph.builder import get_graph
from backend.graph.algorithms import get_connections

router = APIRouter(prefix="/account")

@router.get("/{account_id}")
def get_account_details(account_id: str):
    """
    Returns full investigation snapshot for a specific account.
    Fulfills the 'Account Investigation Panel' requirement.
    """
    profile = get_profile(account_id)
    if profile["transaction_count"] == 0:
        # Check if it exists in the graph even if behavior profile is empty
        g = get_graph()
        if account_id not in g:
            raise HTTPException(status_code=404, detail="Account not found")

    g = get_graph()
    connections = get_connections(g, account_id)
    
    # Identify associated users (Synthetic Identity signals)
    associated_users = set()
    for device_id in profile.get("devices", {}).keys():
        if device_id != "unknown":
            users = get_device_users(device_id)
            associated_users.update(users)
    
    # Remove self from associated users
    if account_id in associated_users:
        associated_users.remove(account_id)

    return {
        "account_id": account_id,
        "transaction_count": profile["transaction_count"],
        "total_volume": profile["total_amount"],
        "risk_history": profile["recent_risk_scores"],
        "graph_connections": connections,
        "behavior_snapshot": {
            "top_locations": sorted(profile["locations"].items(), key=lambda x: x[1], reverse=True)[:3],
            "top_devices": sorted(profile["devices"].items(), key=lambda x: x[1], reverse=True)[:3],
            "transaction_hours_counts": profile["transaction_hours"]
        },
        "synthetic_identity_signals": {
            "shared_hardware_users": list(associated_users),
            "identity_count": len(associated_users)
        },
        "is_active": profile["transaction_count"] > 0
    }
