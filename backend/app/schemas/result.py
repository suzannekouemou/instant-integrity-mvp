from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ResultResponse(BaseModel):
    id: UUID
    sample_id: UUID
    status: str
    confidence: float
    model_version: str
    summary: str | None
    created_at: datetime

    class Config:
        from_attributes = True
