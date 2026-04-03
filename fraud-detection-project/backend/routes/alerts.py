from fastapi import APIRouter
from backend.services.alert_service import fetch_all_alerts

router = APIRouter()

@router.get("/alerts")
def get_alerts():
    return {"alerts": fetch_all_alerts()}