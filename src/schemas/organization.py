from pydantic import Field, RootModel, constr


class OrganizationId(RootModel[constr(max_length=100)]):
    root: constr(max_length=100) = Field( # type: ignore
        ...,
        description='Уникальный идентификатор организации, присвоенный сервером.',
        examples=['550e8400-e29b-41d4-a716-446655440000'],
    )