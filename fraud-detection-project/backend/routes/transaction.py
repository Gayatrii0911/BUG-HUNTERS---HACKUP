from fastapi import APIRouter
from backend.services.transaction_service import process_transaction
from backend.schemas.transaction import TransactionRequest, TransactionResponse

router = APIRouter()

@router.post("/transaction", response_model=TransactionResponse)
def create_transaction(data: TransactionRequest):
    """
    Real-time transaction scoring endpoint (Elite).
    Synchronously processes Graph, ML, and Behavioral intelligence.
    Returns: A complete Section 9 compliant decision object.
    """
    # data.dict() handles the conversion from Pydantic model to a raw dict
    result = process_transaction(data.dict())
    return result
