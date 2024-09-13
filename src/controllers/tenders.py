from http.client import HTTPException
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete, join, select
from src.schemas.enums import TenderServiceType, TenderStatus
from src.db.models.models import Employee, OrganizationResponsible, Tender
from src.schemas.tender import TenderCreate
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



