from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models.models import (
    Employee,
    OrganizationResponsible,
    Tender,
)


async def check_if_user_in_organization(
    session: AsyncSession, username: str, tender: Tender
):
    org_query = (
        select(Employee)
        .join(OrganizationResponsible, Employee.id == OrganizationResponsible.user_id)
        .where(Employee.username == username)
        .where(OrganizationResponsible.organization_id == tender.organization_id)
    )
    user_in_org = await session.execute(org_query)
    user = user_in_org.scalars().first()
    return user


async def get_users_by_organization(session: AsyncSession, organization_id: UUID):
    stmt = select(OrganizationResponsible.user_id).filter(
        OrganizationResponsible.organization_id == organization_id
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_organization_id_by_username(session: AsyncSession, username: str):
    stmt = (
        select(OrganizationResponsible.organization_id)
        .join(Employee)
        .filter(Employee.id == OrganizationResponsible.user_id)
    )
    result = await session.execute(stmt)
    organization_id = result.scalars().first()
    if organization_id is None:
        raise HTTPException(
            status_code=404, detail="Organization for this username not found"
        )
    return organization_id
