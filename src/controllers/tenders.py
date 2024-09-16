from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas.enums import TenderServiceType, TenderStatus
from src.db.models.models import (
    Employee,
    OrganizationResponsible,
    Tender,
    TenderHistory,
)
from src.schemas.tender import TenderCreate, TenderUpdate
from src.controllers.user_organization import (
    check_if_user_in_organization,
)


async def create_tender_history(session: AsyncSession, new_tender: Tender):
    new_tender_history = TenderHistory(
        tender_id=new_tender.id,
        name=new_tender.name,
        service_type=new_tender.service_type,
        status=new_tender.status,
        creator_username=new_tender.creator_username,
        version=new_tender.version,
        description=new_tender.description,
        organization_id=new_tender.organization_id,
    )
    session.add(new_tender_history)
    try:
        await session.commit()
        await session.refresh(new_tender_history)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while writing tender in history",
        )
    return new_tender_history


async def create_tender(session: AsyncSession, tender: TenderCreate) -> Tender:
    new_tender = Tender(**tender.model_dump())
    session.add(new_tender)
    try:
        await session.commit()
        await session.refresh(new_tender)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong organization id"
        )

    await create_tender_history(session, new_tender)

    return new_tender


async def get_tender_list(
    session: AsyncSession,
    limit: int | None,
    offset: int | None,
    service_type: List[TenderServiceType] | None,
) -> List[Tender]:
    query = select(Tender).limit(limit).offset(offset)
    if service_type:
        query = query.filter(Tender.service_type.in_(service_type))
    result = await session.execute(query)
    return result.scalars().all()


async def get_tenders_by_user(
    session: AsyncSession, limit: int | None, offset: int | None, username: str | None
):
    query = (
        select(Tender)
        .join(
            OrganizationResponsible,
            Tender.organization_id == OrganizationResponsible.organization_id,
        )
        .join(Employee, OrganizationResponsible.user_id == Employee.id)
        .filter(Employee.username == username)
        .order_by(Tender.name.asc())
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(query)
    tenders = result.scalars().all()

    return tenders


async def get_tender_by_id(session: AsyncSession, tender_id: UUID):
    query = select(Tender).where(Tender.id == tender_id)

    result = await session.execute(query)
    tender = result.scalars().first()

    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    return tender


async def get_tender_by_id_for_user(
    session: AsyncSession, tender_id: UUID, username: str | None
):
    tender = await get_tender_by_id(session, tender_id)

    if tender.status == TenderStatus.Published:
        return tender
    if username is None:
        raise HTTPException(status_code=403, detail="Access denied")

    # Проверяем, связан ли пользователь с организацией
    user = await check_if_user_in_organization(session, username, tender)

    if user is None:
        raise HTTPException(status_code=403, detail="Access denied")
    return tender


async def change_tender_status_by_id(
    session: AsyncSession, tender_id: UUID, username: str, new_status: TenderStatus
):
    query = select(Tender).where(Tender.id == tender_id)
    result = await session.execute(query)
    tender = result.scalars().first()

    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    if username is None:
        raise HTTPException(status_code=403, detail="Username not specified")

    # Проверяем, связан ли пользователь с организацией
    user = await check_if_user_in_organization(session, username, tender)

    if not user:
        raise HTTPException(status_code=403, detail="Access denied")

    tender.status = new_status
    try:
        await session.commit()
        await session.refresh(tender)
        return tender
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error changing tender status",
        )


async def edit_tender(
    session: AsyncSession, tender_update: TenderUpdate, tender_id: UUID, username: str
):
    query = select(Tender).where(Tender.id == tender_id)
    result = await session.execute(query)
    tender = result.scalars().first()

    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    if username is None:
        raise HTTPException(status_code=403, detail="Username not specified")

    # Проверяем, связан ли пользователь с организацией
    user = await check_if_user_in_organization(session, username, tender)

    if not user:
        raise HTTPException(status_code=403, detail="Access denied")

    for key, val in tender_update.model_dump(exclude_unset=True).items():
        setattr(tender, key, val)
    tender.version += 1
    try:
        await session.commit()
        await session.refresh(tender)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error changing tender status",
        )

    await create_tender_history(session, tender)
    return tender


async def rollback(session: AsyncSession, tender_id: UUID, version: int, username: str):
    tender = await get_tender_by_id_for_user(session, tender_id, username)

    user = await check_if_user_in_organization(session, username, tender)
    if not user:
        raise HTTPException(status_code=403, detail="Access denied")

    history_stmt = select(TenderHistory).filter_by(tender_id=tender_id, version=version)
    history_result = await session.execute(history_stmt)
    tender_history = history_result.scalar_one_or_none()
    if not tender_history:
        raise HTTPException(
            status_code=404, detail="Tender with such version not found"
        )

    for key, val in vars(tender_history).items():
        if key in ["id", "_sa_instance_state"]:
            continue
        if key == "version":
            setattr(tender, key, tender.version + 1)
        else:
            setattr(tender, key, val)

    session.add(tender)
    await session.commit()
    await session.refresh(tender)
    return tender
