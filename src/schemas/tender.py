import datetime
from uuid import UUID
from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    conint,
    field_validator,
)
from pydantic.alias_generators import to_camel
import rfc3339
from src.schemas.enums import TenderServiceType, TenderStatus


class TenderBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    service_type: TenderServiceType

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TenderCreate(TenderBase):
    organization_id: UUID
    creator_username: str


class TenderUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)
    service_type: TenderServiceType | None = Query(None)

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TenderResponse(BaseModel):
    id: UUID
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    status: TenderStatus
    service_type: TenderServiceType
    version: conint(ge=1)  # type: ignore
    created_at: datetime.datetime

    @field_validator("created_at", mode="before")
    def to_rfc3339(cls, date):
        return rfc3339.rfc3339(date)

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=False
    )
