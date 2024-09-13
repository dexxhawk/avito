from pydantic import BaseModel


class ErrorResponseBase(BaseModel):
    reason: str | None
