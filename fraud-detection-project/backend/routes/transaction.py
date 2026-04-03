from fastapi import APIRouter
from backend.services.transaction_service import process_transaction
from backend.models.schemas import TransactionRequest

router = APIRouter()

@router.post("/transaction")
def create_transaction(data: TransactionRequest):
    """
    Real-time transaction scoring endpoint.
    Synchronously processes Graph, ML, and Behavioral intelligence.
    """
    # data.dict() handles the conversion from Pydantic model to the dict expected by service
    result = process_transaction(data.dict())
    return result
