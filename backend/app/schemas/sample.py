from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class SampleType(str, Enum):
    flour = "flour"
    spice = "spice"
    herb = "herb"
    other = "other"


class SampleUpload(BaseModel):
    sample_type: SampleType
    filename: str = Field(max_length=255)


class SampleResponse(BaseModel):
    id: UUID
    user_id: UUID
    filename: str
    sample_type: str
    created_at: datetime

    class Config:
        from_attributes = True
