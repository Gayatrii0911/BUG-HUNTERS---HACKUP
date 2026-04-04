from pydantic import BaseModel, Field
from typing import Optional, List, Dict

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
    reasons: List[Dict[str, str]]
    reason_categories: Optional[Dict[str, List[Dict[str, str]]]] = None
    score_breakdown: Dict[str, float]
    anomaly_score: float
    anomaly_level: str
    confidence: float
    fraud_chain_detected: bool
    is_pre_transaction_check: bool = True
    alert: bool
    alert_id: Optional[str] = None