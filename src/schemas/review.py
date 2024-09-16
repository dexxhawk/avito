import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, constr
from pydantic.alias_generators import to_camel


class FeedbackResponse(BaseModel):
    id: UUID
    description: constr(max_length=1000)
    created_at: datetime.datetime

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=False
    )
