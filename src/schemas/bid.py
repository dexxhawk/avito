import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.schemas.enums import BidStatus

class BidBase(BaseModel):
  name: str
  description: str
  status: BidStatus
  tender_id: UUID
  organization_id: UUID
  creator_username: str

class BidCreate(BidBase):
    pass


class BidResponse(BidBase):
    ...
    model_config = ConfigDict(from_attributes=True)


