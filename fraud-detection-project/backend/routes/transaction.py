from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.services.transaction_service import process_transaction

router = APIRouter()

class TransactionRequest(BaseModel):
    transaction_id: Optional[str] = None
    sender_id: str
    receiver_id: str
    amount: float
    device_id: Optional[str] = "unknown"
    location: Optional[str] = "unknown"
    channel: Optional[str] = "web"
    timestamp: Optional[str] = None

@router.post("/transaction")
def create_transaction(data: TransactionRequest):
    result = process_transaction(data.dict())
    return result
