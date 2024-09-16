import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, RootModel, conint, constr
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


# class BidId(RootModel[constr(max_length=100)]):
#     root: constr(max_length=100) = Field( # type: ignore
#         ...,
#         description='Уникальный идентификатор предложения, присвоенный сервером.',
#         examples=['550e8400-e29b-41d4-a716-446655440000'],
#     )


# class BidName(RootModel[constr(max_length=100)]):
#     root: constr(max_length=100) = Field(..., description='Полное название предложения') # type: ignore


# class BidDescription(RootModel[constr(max_length=500)]):
#     root: constr(max_length=500) = Field(..., description='Описание предложения') # type: ignore


# class BidFeedback(RootModel[constr(max_length=1000)]):
#     root: constr(max_length=1000) = Field(..., description='Отзыв на предложение') # type: ignore


# class BidAuthorId(RootModel[constr(max_length=100)]):
#     root: constr(max_length=100) = Field( # type: ignore
#         ...,
#         description='Уникальный идентификатор автора предложения, присвоенный сервером.',
#         examples=['550e8400-e29b-41d4-a716-446655440000'],
#     )


# class BidVersion(RootModel[conint(ge=1)]):
#     root: conint(ge=1) = Field(..., description='Номер версии посел правок') # type: ignore


# class BidReviewId(RootModel[constr(max_length=100)]):
#     root: constr(max_length=100) = Field( # type: ignore
#         ...,
#         description='Уникальный идентификатор отзыва, присвоенный сервером.',
#         examples=['550e8400-e29b-41d4-a716-446655440000'],
#     )


# class BidReviewDescription(RootModel[constr(max_length=1000)]):
#     root: constr(max_length=1000) = Field(..., description='Описание предложения') # type: ignore


# class BidReview(BaseModel):
#     id: BidReviewId
#     description: BidReviewDescription
#     createdAt: str = Field(
#         ...,
#         description='Серверная дата и время в момент, когда пользователь отправил отзыв на предложение.\nПередается в формате RFC3339.\n',
#         examples=['2006-01-02T15:04:05Z07:00'],
#     )