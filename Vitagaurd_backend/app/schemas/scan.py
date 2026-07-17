from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict
from enum import Enum


class Verdict(str, Enum):
    genuine = "Genuine"
    suspicious = "Suspicious"
    likely_fake = "Likely Fake"


class ScanRequest(BaseModel):
    product_id: UUID
    batch_number: str = Field(..., min_length=3, max_length=50)
    location: str = Field(..., min_length=2, max_length=100)

    device_id: str = Field(..., min_length=3, max_length=100)
    user_id: Optional[UUID] = None

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    scan_timestamp: Optional[datetime] = None


class ScanResponse(BaseModel):
    scan_id: UUID
    risk_score: float
    verdict: Verdict

    expired: bool
    product_found: bool
    batch_found: bool

    risk_breakdown: Dict[str, float]

    reason: str
    timestamp: datetime