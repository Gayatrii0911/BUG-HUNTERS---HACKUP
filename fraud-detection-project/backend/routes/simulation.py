from fastapi import APIRouter, HTTPException
from backend.services.simulation_service import run_scenario
from backend.db.database import reset_all_db

router = APIRouter(prefix="/simulation")

@router.post("/run/{scenario_name}")
def execute_scenario(scenario_name: str):
    try:
        results = run_scenario(scenario_name)
        return {"status": "success", "scenario": scenario_name, "steps": len(results), "results": results}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
def reset_system():
    """Wipes all databases and graph state for a fresh demo."""
    from backend.graph.graph_store import reset_graph
    from backend.behavior.profile_store import reset_profiles
    from backend.alerts.store import clear_alerts
    from backend.behavior.behavioral_analyzer import reset_behavior_engine
    
    reset_graph()
    reset_profiles()
    clear_alerts()
    reset_behavior_engine()
    reset_all_db()
    
    return {"status": "ok", "message": "All backend states reset"}

@router.get("/scenarios")
def list_scenarios():
    """Returns all ready-to-run demo scenarios."""
    return {
        "scenarios": [
            {"id": "normal", "name": "Normal Usage", "description": "Baseline consumer behavior with low anomaly profile."},
            {"id": "cycle", "name": "Cycle Fraud", "description": "Closed-loop fund rotation (A -> B -> C -> A)."},
            {"id": "hub", "name": "Mule Hub", "description": "High-fan-in node rapidly receiving funds from many sources."},
            {"id": "relay", "name": "Prof. Relay", "description": "Rapid pass-through node used for money laundering layering."},
            {"id": "chain", "name": "Laundering Chain", "description": "Deep multi-hop fund flow across 5+ accounts."},
            {"id": "smurfing", "name": "Structuring", "description": "Multiple rapid sub-threshold transactions to evade AML."},
            {"id": "ato", "name": "Account Takeover", "description": "High-velocity identity theft with environment shift."},
            {"id": "cluster", "name": "Fraud Ring", "description": "A dense, isolated cluster of high-intensity activity."}
        ]
    }
