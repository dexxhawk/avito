# generated by datamodel-codegen:
#   filename:  openapi.yml
#   timestamp: 2024-09-12T23:35:51+00:00

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, conint, constr


class Username(BaseModel):
    __root__: str = Field(
        ..., description="Уникальный slug пользователя.", example="test_user"
    )


class TenderStatus(Enum):
    Created = "Created"
    Published = "Published"
    Closed = "Closed"


class TenderServiceType(Enum):
    Construction = "Construction"
    Delivery = "Delivery"
    Manufacture = "Manufacture"


class TenderId(BaseModel):
    __root__: constr(max_length=100) = Field(
        ...,
        description="Уникальный идентификатор тендера, присвоенный сервером.",
        example="550e8400-e29b-41d4-a716-446655440000",
    )


class TenderName(BaseModel):
    __root__: constr(max_length=100) = Field(..., description="Полное название тендера")


class TenderDescription(BaseModel):
    __root__: constr(max_length=500) = Field(..., description="Описание тендера")


class TenderVersion(BaseModel):
    __root__: conint(ge=1) = Field(..., description="Номер версии посел правок")


class OrganizationId(BaseModel):
    __root__: constr(max_length=100) = Field(
        ...,
        description="Уникальный идентификатор организации, присвоенный сервером.",
        example="550e8400-e29b-41d4-a716-446655440000",
    )


class Tender(BaseModel):
    id: TenderId
    name: TenderName
    description: TenderDescription
    serviceType: TenderServiceType
    status: TenderStatus
    organizationId: OrganizationId
    version: TenderVersion
    createdAt: str = Field(
        ...,
        description="Серверная дата и время в момент, когда пользователь отправил тендер на создание.\nПередается в формате RFC3339.\n",
        example="2006-01-02T15:04:05Z07:00",
    )


class BidStatus(Enum):
    Created = "Created"
    Published = "Published"
    Canceled = "Canceled"
    Approved = "Approved"
    Rejected = "Rejected"


class BidDecision(Enum):
    Approved = "Approved"
    Rejected = "Rejected"


class BidId(BaseModel):
    __root__: constr(max_length=100) = Field(
        ...,
        description="Уникальный идентификатор предложения, присвоенный сервером.",
        example="550e8400-e29b-41d4-a716-446655440000",
    )


class BidName(BaseModel):
    __root__: constr(max_length=100) = Field(
        ..., description="Полное название предложения"
    )


class BidDescription(BaseModel):
    __root__: constr(max_length=500) = Field(..., description="Описание предложения")


class BidFeedback(BaseModel):
    __root__: constr(max_length=1000) = Field(..., description="Отзыв на предложение")


class BidAuthorType(Enum):
    Organization = "Organization"
    User = "User"


class BidAuthorId(BaseModel):
    __root__: constr(max_length=100) = Field(
        ...,
        description="Уникальный идентификатор автора предложения, присвоенный сервером.",
        example="550e8400-e29b-41d4-a716-446655440000",
    )


class BidVersion(BaseModel):
    __root__: conint(ge=1) = Field(..., description="Номер версии посел правок")


class BidReviewId(BaseModel):
    __root__: constr(max_length=100) = Field(
        ...,
        description="Уникальный идентификатор отзыва, присвоенный сервером.",
        example="550e8400-e29b-41d4-a716-446655440000",
    )


class BidReviewDescription(BaseModel):
    __root__: constr(max_length=1000) = Field(..., description="Описание предложения")


class BidReview(BaseModel):
    id: BidReviewId
    description: BidReviewDescription
    createdAt: str = Field(
        ...,
        description="Серверная дата и время в момент, когда пользователь отправил отзыв на предложение.\nПередается в формате RFC3339.\n",
        example="2006-01-02T15:04:05Z07:00",
    )


class Bid(BaseModel):
    id: BidId
    name: BidName
    description: BidDescription
    status: BidStatus
    tenderId: TenderId
    authorType: BidAuthorType
    authorId: BidAuthorId
    version: BidVersion
    createdAt: str = Field(
        ...,
        description="Серверная дата и время в момент, когда пользователь отправил предложение на создание.\nПередается в формате RFC3339.\n",
        example="2006-01-02T15:04:05Z07:00",
    )


class ErrorResponse(BaseModel):
    reason: constr(min_length=5) = Field(
        ..., description="Описание ошибки в свободной форме"
    )
