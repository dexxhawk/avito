from pydantic import Field, RootModel


class Username(RootModel[str]):
    root: str = Field(
        ..., description="Уникальный slug пользователя.", examples=["test_user"]
    )
