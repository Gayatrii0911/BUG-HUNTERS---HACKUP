from fastapi import APIRouter
from backend.graph.builder import reset_graph

router = APIRouter(prefix="/debug")

@router.post("/reset")
def reset_system():
    """Clears the in-memory graph for testing."""
    reset_graph()
    return {"status": "success", "message": "Graph reset successful"}

@router.get("/ping")
def ping():
    return {"message": "debug router is active"}
