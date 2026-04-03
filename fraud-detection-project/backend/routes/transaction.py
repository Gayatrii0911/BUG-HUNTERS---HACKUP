
from fastapi import APIRouter
from backend.schemas.transaction import TransactionRequest, TransactionResponse

router = APIRouter()

@router.post("/transaction", response_model=TransactionResponse)
def submit_transaction(tx: TransactionRequest):
    # Phase 1 will wire the service here
    return TransactionResponse(
        risk_score=0,
        risk_level="low",
        decision="APPROVE",
        reasons=[],
        alert=False
    )