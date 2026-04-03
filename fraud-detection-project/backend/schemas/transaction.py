from pydantic import BaseModel
from typing import List
from datetime import datetime


class TransactionRequest(BaseModel):
    user_id: str
    from_account: str
    to_account: str
    amount: float
    timestamp: datetime
    device_id: str
    channel: str
    location: str


class TransactionResponse(BaseModel):
    risk_score: float
    risk_level: str
    decision: str
    reasons: List[str]
    alert: bool