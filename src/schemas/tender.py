import datetime
from uuid import UUID
from fastapi import Query
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, conint
from pydantic.alias_generators import to_snake, to_camel

from src.schemas.enums import TenderServiceType, TenderStatus


class TenderBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    service_type: TenderServiceType
    status: TenderStatus

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class TenderCreate(TenderBase):
    organization_id: UUID
    creator_username: str


class TenderUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)
    service_type: TenderServiceType | None = Query(None)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class TenderResponse(TenderBase):
    id: UUID
    version: conint(ge=1)
    created_at: datetime.datetime

    # class Config:
    #     alias_generator = to_camel
    #     populate_by_name = True
    #     from_attributes = True
