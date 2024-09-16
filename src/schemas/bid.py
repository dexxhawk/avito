import datetime
from uuid import UUID
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)
from pydantic.alias_generators import to_camel
from src.schemas.enums import BidAuthorType, BidStatus
import rfc3339


class BidBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    # status: BidStatus

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BidCreate(BidBase):
    tender_id: UUID
    author_type: BidAuthorType
    author_id: UUID


class BidUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)


class BidResponse(BaseModel):
    id: UUID
    name: str
    status: BidStatus
    author_type: BidAuthorType
    author_id: UUID
    version: int
    created_at: datetime.datetime

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=False
    )

    @field_validator("created_at", mode="before")
    def to_rfc3339(cls, date):
        return rfc3339.rfc3339(date)
