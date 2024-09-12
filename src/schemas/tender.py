import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.schemas.enums import TenderServiceType, TenderStatus

class TenderBase(BaseModel):
    name: str
    description: str
    service_type: TenderServiceType
    status: TenderStatus

class TenderCreate(TenderBase):
    organization_id: UUID
    creator_username: str


class TenderResponse(TenderBase):
    id: UUID
    version: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)


