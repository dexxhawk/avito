import datetime
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, RootModel, conint, constr
from pydantic.alias_generators import to_camel

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
    version: conint(ge=1) # type: ignore
    created_at: datetime.datetime

    # class Config:
    #     alias_generator = to_camel
    #     populate_by_name = True
    #     from_attributes = True


# class TenderId(RootModel[constr(max_length=100)]):
#     root: constr(max_length=100) = Field( # type: ignore
#         ...,
#         description='Уникальный идентификатор тендера, присвоенный сервером.',
#         examples=['550e8400-e29b-41d4-a716-446655440000'],
#     )

# class TenderName(RootModel[constr(max_length=100)]):
#     root: constr(max_length=100) = Field(..., description='Полное название тендера') # type: ignore


# class TenderDescription(RootModel[constr(max_length=500)]):
#     root: constr(max_length=500) = Field(..., description='Описание тендера') # type: ignore


# class TenderVersion(RootModel[conint(ge=1)]):
#     root: conint(ge=1) = Field(..., description='Номер версии посел правок') # type: ignore