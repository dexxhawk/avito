import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, constr, field_validator
from pydantic.alias_generators import to_camel
import rfc3339


class FeedbackResponse(BaseModel):
    id: UUID
    description: constr(max_length=1000)
    created_at: datetime.datetime

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=False
    )

    @field_validator("created_at", mode="before")
    def to_rfc3339(cls, date):
        return rfc3339.rfc3339(date)
