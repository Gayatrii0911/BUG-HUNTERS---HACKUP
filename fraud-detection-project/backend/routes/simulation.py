from fastapi import APIRouter
from backend.services.simulation_service import SimulationService
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class SimulationRequest(BaseModel):
    pattern: str # "normal", "ato", "fraud_ring"
    count: Optional[int] = 10

@router.post("/simulate")
def trigger_simulation(request: SimulationRequest):
    if request.pattern == "normal":
        results = SimulationService.run_normal_wave(request.count)
    elif request.pattern == "ato":
        results = SimulationService.run_ato_attack()
    elif request.pattern == "fraud_ring":
        results = SimulationService.run_fraud_ring(request.count)
    else:
        return {"error": "Invalid pattern"}
    
    return {"message": f"Simulation of {request.pattern} completed.", "count": len(results)}
