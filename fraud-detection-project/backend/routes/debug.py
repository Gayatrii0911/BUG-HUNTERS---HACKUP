from fastapi import APIRouter

router = APIRouter()

@router.get("/debug/ping")
def ping():
    return {"message": "debug router is active"}
