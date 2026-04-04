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
    from backend.graph.builder import reset_graph
    from backend.behavior.profile_store import reset_profiles
    from backend.alerts.store import clear_alerts
    
    reset_graph()
    reset_profiles()
    clear_alerts()
    reset_all_db()
    
    return {"status": "ok", "message": "All backend states reset"}
