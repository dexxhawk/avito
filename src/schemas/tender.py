import datetime
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, conint

from src.schemas.enums import TenderServiceType, TenderStatus


class TenderBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    service_type: TenderServiceType
    status: TenderStatus


class TenderCreate(TenderBase):
    organization_id: UUID
    creator_username: str


class TenderUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)
    service_type: TenderServiceType | None = Query(None)


class TenderResponse(TenderBase):
    id: UUID
    version: conint(ge=1)
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)
