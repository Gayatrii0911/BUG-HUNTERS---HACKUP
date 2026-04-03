from pydantic import BaseModel, Field, validator
from typing import Optional

class TransactionRequest(BaseModel):
    sender_id: str = Field(..., alias="sender_id")
    receiver_id: str = Field(..., alias="receiver_id")
    amount: float = Field(..., gt=0, description="Amount must be positive")
    timestamp: Optional[str] = None
    device_id: str = "unknown"
    location: str = "unknown"
    channel: str = "web"

    class Config:
        populate_by_name = True

class TransactionResponse(BaseModel):
    transaction_id: str
    risk_score: float
    risk_level: str
    decision: str
    reasons: list
    score_breakdown: dict
    anomaly_score: float
    anomaly_level: str
    fraud_chain_detected: bool
    is_pre_transaction_check: bool = True
    alert: bool
    alert_id: str
