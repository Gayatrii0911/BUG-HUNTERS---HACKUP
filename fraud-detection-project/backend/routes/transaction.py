

from fastapi import APIRouter
from backend.schemas.transaction import TransactionRequest, TransactionResponse
from backend.services.transaction_service import process_transaction

router = APIRouter()

@router.post("/transaction", response_model=TransactionResponse)
def submit_transaction(tx: TransactionRequest):
    result = process_transaction(tx)
    return TransactionResponse(**result)
