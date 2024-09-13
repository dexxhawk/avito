from http.client import HTTPException
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete, join, or_, select
from src.schemas.enums import TenderServiceType, TenderStatus
from src.db.models.models import Employee, OrganizationResponsible, Tender
from src.schemas.tender import TenderCreate, TenderUpdate
from src.schemas.response import ErrorResponseBase


async def create_tender(session: AsyncSession, tender: TenderCreate) -> Tender:
    new_tender = Tender(**tender.model_dump())
    session.add(new_tender)
    try:
        await session.commit()
        await session.refresh(new_tender)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось создать данный тендер"
        )
    return new_tender


async def get_tender_list(session: AsyncSession, limit: int, offset: int, service_type: List[TenderServiceType] | None) -> List[Tender]:
    query = select(Tender).limit(limit).offset(offset)
    if service_type:
        query = query.filter(Tender.service_type.in_(service_type))
    result = await session.execute(query)
    return result.scalars().all()

# async def get_user_tenders(session: AsyncSession):
#     query = select(Tender).
#     result = await session.execute(query)
#     return result.scalars().all()


async def get_tender(session: AsyncSession, tender_id: int) -> Tender:
    query = select(Tender).filter(Tender.id == tender_id)
    result = await session.execute(query)
    return result.scalars().first()

# async def change_tender_status(session: AsyncSession, tender_id: int, status: TenderStatus):
#     query = select(Tender).filter(Tender.id == tender_id)
#     result = await session.execute(query)
#     tender = result.scalars().first()
#     setattr(tender, status, status)


async def get_tenders_by_user(session: AsyncSession, limit: int, offset: int, username: str):
    query = (
        select(Tender)
        .join(OrganizationResponsible, Tender.organization_id == OrganizationResponsible.organization_id)
        .join(Employee, OrganizationResponsible.user_id == Employee.id)
        .filter(Employee.username == username)
        .limit(limit)
        .offset(offset)
    )
    
    result = await session.execute(query)
    tenders = result.scalars().all()
    
    return tenders


async def get_tender_by_id(
    session: AsyncSession, tender_id: str, username: Optional[str] = None
):
    query = select(Tender).where(Tender.id == tender_id)
    
    result = await session.execute(query)
    tender = result.scalars().first()

    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")
    
    if tender.status == "Published":
            return tender
    if username is None:
        raise HTTPException(status_code=403, detail="Access denied")

    # Проверяем, связан ли пользователь с организацией
    org_query = (
        select(Employee)
        .join(OrganizationResponsible, Employee.id == OrganizationResponsible.user_id)
        .where(Employee.username == username)
        .where(OrganizationResponsible.organization_id == tender.organization_id)
    )
    user_in_org = await session.execute(org_query)
    user = user_in_org.scalars().first()

    if user:
        return tender
    else:
        raise HTTPException(status_code=403, detail="Access denied")


async def change_tender_status_by_id(
    session: AsyncSession, tender_id: str, username: str, new_status: TenderStatus
):
    query = select(Tender).where(Tender.id == tender_id)
    result = await session.execute(query)
    tender = result.scalars().first()

    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    if username is None:
        raise HTTPException(status_code=403, detail="Username not specified")

    # Проверяем, связан ли пользователь с организацией
    org_query = (
        select(Employee)
        .join(OrganizationResponsible, Employee.id == OrganizationResponsible.user_id)
        .where(Employee.username == username)
        .where(OrganizationResponsible.organization_id == tender.organization_id)
    )
    user_in_org = await session.execute(org_query)
    user = user_in_org.scalars().first()

    if user:
        tender.status = new_status
        try:
            await session.commit()
            await session.refresh(tender)
            return tender
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error changing tender status")

    else:
        raise HTTPException(status_code=403, detail="Access denied")
    

async def edit_tender(
    session: AsyncSession, tender_update: TenderUpdate, tender_id: str, username: str
):
    query = select(Tender).where(Tender.id == tender_id)
    result = await session.execute(query)
    tender = result.scalars().first()

    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    if username is None:
        raise HTTPException(status_code=403, detail="Username not specified")

    # Проверяем, связан ли пользователь с организацией
    org_query = (
        select(Employee)
        .join(OrganizationResponsible, Employee.id == OrganizationResponsible.user_id)
        .where(Employee.username == username)
        .where(OrganizationResponsible.organization_id == tender.organization_id)
    )
    user_in_org = await session.execute(org_query)
    user = user_in_org.scalars().first()

    if user:
        for key, val in tender_update.model_dump(exclude_unset=True).items():
            setattr(tender, key, val)
        try:
            await session.commit()
            await session.refresh(tender)
            return tender
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error changing tender status")

    else:
        raise HTTPException(status_code=403, detail="Access denied")