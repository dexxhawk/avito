import asyncio
import random
from faker import Faker
from src.db.models.models import Employee, Organization, OrganizationResponsible
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import get_settings

engine = create_async_engine(
    get_settings().database_uri,
    echo=True,
    future=True,
)

session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def fill_employee_organizations():
    fake = Faker()
    async with session_maker() as session:
        for _ in range(100):
            employee = Employee(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            organization = Organization(
                name=fake.company(),
                description=fake.text(100),
                type=random.choice(["IE", "LLC", "JSC"]),
            )
            session.add(employee)
            session.add(organization)
            await session.commit()
            session.refresh(employee)
            session.refresh(organization)
            organization_responsible = OrganizationResponsible(
                organization_id=organization.id, user_id=employee.id
            )
            session.add(organization_responsible)
            await session.commit()


async def clean(obj):
    async with session_maker() as session:
        result = await session.execute(select(obj))
        models = result.scalars().all()

        for model in models:
            await session.delete(model)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(fill_employee_organizations())
    # asyncio.run(clean(Employee))
    # asyncio.run(clean(Organization))
    # asyncio.run(clean(OrganizationResponsible))
