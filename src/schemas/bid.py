import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from src.schemas.enums import BidAuthorType, BidStatus


class BidBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    status: BidStatus

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

class BidCreate(BidBase):
    tender_id: UUID
    organization_id: UUID
    creator_username: str


class BidUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)


class BidResponse(BidBase):
    id: UUID
    name: str
    status: BidStatus
    author_type: BidAuthorType
    author_id: UUID
    version: int
    created_at: datetime.datetime 

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=False
    )
