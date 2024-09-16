from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import join, select
from src.schemas.enums import BidDecision, BidStatus
from src.db.models.models import (
    Bid,
    BidHistory,
    Employee,
    Feedback,
    Organization,
    OrganizationResponsible,
    Tender,
)
from src.schemas.bid import BidCreate, BidUpdate
from src.schemas.enums import BidDecision


async def create_bid_history(session: AsyncSession, new_bid: Bid):
    new_bid_history = BidHistory(
        bid_id=new_bid.id,
        name=new_bid.name,
        status=new_bid.status,
        tender_id=new_bid.tender_id,
        organization_id=new_bid.organization_id,
        creator_username=new_bid.creator_username,
        version=new_bid.version,
        description=new_bid.description,
    )
    session.add(new_bid_history)
    # try:
    await session.commit()
    await session.refresh(new_bid_history)
    # except IntegrityError:
    # await session.rollback()
    # raise HTTPException(
    # status_code=status.HTTP_400_BAD_REQUEST,
    # detail="Error while writing bid in history"
    # )
    return new_bid_history


async def create_bid(session: AsyncSession, bid: BidCreate) -> BidCreate:
    new_bid = Bid(**bid.model_dump())
    session.add(new_bid)
    try:
        await session.commit()
        await session.refresh(new_bid)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось создать данное предложение",
        )
    await create_bid_history(session, new_bid)
    return new_bid


async def get_bids_by_user(
    session: AsyncSession, limit: int | None, offset: int | None, username: str
):
    query = (
        select(Bid)
        .select_from(
            join(Bid, Tender, Bid.tender_id == Tender.id)
            .join(Organization, Tender.organization_id == Organization.id)
            .join(
                OrganizationResponsible,
                Organization.id == OrganizationResponsible.organization_id,
            )
            .join(Employee, OrganizationResponsible.user_id == Employee.id)
        )
        .filter(Bid.creator_username == username)
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(query)
    bids = result.scalars().all()

    return bids


async def get_bid_by_id(session: AsyncSession, bid_id: UUID, username: str):
    # Проверяем, существует ли Bid с данным bid_id
    bid_query = select(Bid).filter(Bid.id == bid_id)
    bid_result = await session.execute(bid_query)
    bid = bid_result.scalars().first()

    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")

    # Проверяем, есть ли у пользователя доступ (он автор или ответственен за тендер)
    access_query = (
        select(Bid)
        .join(Tender, Bid.tender_id == Tender.id)
        .join(
            OrganizationResponsible,
            Tender.organization_id == OrganizationResponsible.organization_id,
        )
        .join(Employee, OrganizationResponsible.user_id == Employee.id)
        .filter(
            (Bid.id == bid_id)
            & ((Bid.creator_username == username) | (Employee.username == username))
        )
    )

    access_result = await session.execute(access_query)
    accessible_bid = access_result.scalars().first()

    if not accessible_bid:
        raise HTTPException(status_code=403, detail="Access denied")

    return bid


async def change_bid_status(
    session: AsyncSession, bid_id: UUID, new_status: BidStatus, username: str
):
    bid = await get_bid_by_id(session, bid_id, username)

    if not bid:
        raise HTTPException(status_code=403, detail="Access denied")

    bid.status = new_status

    await session.commit()
    await session.refresh(bid)
    return bid


async def edit_bid(
    session: AsyncSession, bid_update: BidUpdate, bid_id: UUID, username: str
):
    bid = await get_bid_by_id(session, bid_id, username)

    if not bid:
        raise HTTPException(status_code=403, detail="Access denied")

    for key, val in bid_update.model_dump(exclude_unset=True).items():
        setattr(bid, key, val)
    bid.version += 1
    try:
        await session.commit()
        await session.refresh(bid)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error changing bid status"
        )

    await create_bid_history(session, bid)
    return bid


async def get_bids_by_tender(
    session: AsyncSession,
    tender_id: UUID,
    username: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> List[Bid]:
    # Проверяем доступ пользователя к тендеру
    access_query = (
        select(Tender)
        .join(
            OrganizationResponsible,
            Tender.organization_id == OrganizationResponsible.organization_id,
        )
        .join(Employee, OrganizationResponsible.user_id == Employee.id)
        .filter(
            (Tender.id == tender_id)
            & ((Tender.creator_username == username) | (Employee.username == username))
        )
    )

    access_result = await session.execute(access_query)
    tender = access_result.scalars().first()

    if not tender:
        raise HTTPException(status_code=403, detail="Access denied")

    # Получаем список предложений, связанных с указанным тендером
    bids_query = (
        select(Bid).filter(Bid.tender_id == tender_id).limit(limit).offset(offset)
    )

    bids_result = await session.execute(bids_query)
    bids = bids_result.scalars().all()

    return bids


async def make_feedback(
    session: AsyncSession, bid_id: UUID, bid_feedback: str, username: str
):
    stmt = select(Bid).where(Bid.id == bid_id)
    result = await session.execute(stmt)
    bid = result.scalars().first()

    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")

    new_feedback = Feedback(
        bid_id=bid_id, feedback=bid_feedback, creator_username=username
    )

    session.add(new_feedback)
    await session.commit()
    await session.refresh(new_feedback)
    return new_feedback


async def get_reviews(
    session: AsyncSession,
    tender_id: UUID,
    author_username: str,
    request_username: str,
    limit: int,
    offset: int,
):
    stmt = (
        select(Employee)
        .join(OrganizationResponsible)
        .join(Organization)
        .join(Tender)
        .filter(Employee.username == author_username)
        .filter(OrganizationResponsible.organization_id == Tender.organization_id)
        .filter(Tender.id == tender_id)
        .distinct()
    )

    result = await session.execute(stmt)
    requester = result.scalars().first()

    if not requester:
        raise HTTPException(status_code=403, detail="Access denied")

    # Query to get feedbacks for the given tender and author
    stmt = (
        select(Feedback)
        .join(Bid)
        .filter(Bid.tender_id == tender_id)
        .filter(Bid.creator_username == author_username)
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(stmt)
    feedbacks = result.scalars().all()

    return feedbacks


async def submit_decision(
    session: AsyncSession, bid_id: UUID, new_desicion: BidDecision, username: str
):
    bid = await get_bid_by_id(session, bid_id, username)
    bid.decision = new_desicion
    await session.commit()
    await session.refresh(bid)
    return bid


async def rollback(session: AsyncSession, bid_id: UUID, version: int, username: str):
    bid = await get_bid_by_id(session, bid_id, username)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")

    history_stmt = select(BidHistory).filter_by(bid_id=bid_id, version=version)
    history_result = await session.execute(history_stmt)
    bid_history = history_result.scalar_one_or_none()
    if not bid_history:
        raise HTTPException(status_code=404, detail="Bid with such version not found")

    for key, val in vars(bid_history).items():
        if key in ["id", "_sa_instance_state"]:
            continue
        if key == "version":
            setattr(bid, key, bid.version + 1)
        else:
            setattr(bid, key, val)

    session.add(bid)
    await session.commit()
    await session.refresh(bid)
    return bid
