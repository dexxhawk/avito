from pydantic import BaseModel, constr


class ErrorResponseBase(BaseModel):
    reason: constr(min_length=5)  # type: ignore
