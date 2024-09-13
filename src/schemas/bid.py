from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from src.schemas.enums import BidStatus


class BidBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    status: BidStatus
    tender_id: UUID
    organization_id: UUID
    creator_username: str


class BidCreate(BidBase):
    pass


class BidUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)


class BidResponse(BidBase):
    model_config = ConfigDict(from_attributes=False)
