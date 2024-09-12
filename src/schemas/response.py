import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.schemas.enums import TenderServiceType, TenderStatus

class ErrorResponseBase(BaseModel):
    reason: str | None

