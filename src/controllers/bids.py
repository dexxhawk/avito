from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, or_, select
from src.controllers.tenders import (
    change_tender_status_by_id,
    get_tender_by_id,
    get_tender_by_id_for_user,
)
from src.schemas.enums import BidDecision, BidStatus, BidAuthorType, TenderStatus
from src.db.models.models import (
    Bid,
    BidHistory,
    Employee,
    Feedback,
    Organization,
    OrganizationResponsible,
    Tender,
    Vote,
)
from src.schemas.bid import BidCreate, BidResponse, BidUpdate
from src.controllers.user_organization import (
    get_user_by_id,
    get_user_by_username,
    get_users_by_organization,
    get_organization_id_by_username,
)


async def create_bid_history(session: AsyncSession, new_bid: Bid):
    new_bid_history = BidHistory(
        bid_id=new_bid.id,
        name=new_bid.name,
        status=new_bid.status,
        tender_id=new_bid.tender_id,
        author_type=new_bid.author_type,
        author_id=new_bid.author_id,
        version=new_bid.version,
        created_at=new_bid.created_at,
        kvorum=new_bid.kvorum,
        votes_qty=new_bid.votes_qty,
        description=new_bid.description,
        decision=new_bid.decision,
    )
    session.add(new_bid_history)
    try:
        await session.commit()
        await session.refresh(new_bid_history)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error while writing bid in history",
        )
    return new_bid_history


async def create_bid(session: AsyncSession, bid: BidCreate) -> BidResponse:
    if bid.author_type == BidAuthorType.Organization:
        stmt = select(Organization.name).filter(Organization.id == bid.author_id)
    else:
        stmt = select(Employee.username).filter(Employee.id == bid.author_id)

    result = await session.execute(stmt)
    _ = result.scalars().first()

    tender = await get_tender_by_id(session, bid.tender_id)

    new_bid = Bid(**bid.model_dump())

    users = await get_users_by_organization(session, tender.organization_id)
    new_bid.kvorum = min(3, len(users))
    new_bid.status = BidStatus.Created
    new_bid.votes_qty = 0
    session.add(new_bid)

    try:
        await session.commit()
        await session.refresh(new_bid)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't create bid with these parameters",
        )
    await create_bid_history(session, new_bid)
    return new_bid


async def get_bids_by_user(
    session: AsyncSession, limit: int | None, offset: int | None, username: str | None
):
    try:
        organization_id = await get_organization_id_by_username(session, username)  # type: ignore
    except HTTPException:
        organization_id = None

    query = (
        select(Bid)
        .outerjoin(Employee, Bid.author_id == Employee.id)
        .outerjoin(
            OrganizationResponsible, Employee.id == OrganizationResponsible.user_id
        )
        .filter(
            or_(
                Employee.username == username,
                OrganizationResponsible.organization_id == organization_id,
            )
        )
        .order_by(Bid.name.asc())
        .limit(limit)
        .offset(offset)
    )

    try:
        result = await session.execute(query)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong username",
        )
    bids = result.scalars().all()

    return bids


async def get_bid_by_id(session: AsyncSession, bid_id: UUID):
    bid_query = select(Bid).filter(Bid.id == bid_id)
    bid_result = await session.execute(bid_query)
    bid = bid_result.scalars().first()

    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")

    return bid


async def get_bid_for_bid_organization(
    session: AsyncSession, bid_id: UUID, username: str
):
    # Кто в организации bid
    bid = await get_bid_by_id(session, bid_id)
    user = await get_user_by_id(session, bid.author_id)
    organization_id = await get_organization_id_by_username(session, user.username)

    stmt = (
        select(OrganizationResponsible.user_id)
        .join(Employee, Employee.id == OrganizationResponsible.user_id)
        .filter(OrganizationResponsible.organization_id == organization_id)
        .filter(Employee.username == username)
    )
    result = await session.execute(stmt)
    user_id = result.scalars().first()

    if user_id is None:
        raise HTTPException(status_code=403, detail="Access denied")

    bid = await get_bid_by_id(session, bid_id)
    if bid is None:
        raise HTTPException(status_code=404, detail="Wrong bid_id")

    return bid


async def get_bid_for_tender_organization(
    session: AsyncSession, bid_id: UUID, username: str
):
    # Кто в организации tender
    stmt = (
        select(Bid)
        .join(Tender, Tender.id == Bid.tender_id)
        .outerjoin(Organization, Organization.id == Tender.organization_id)
        .outerjoin(
            OrganizationResponsible,
            OrganizationResponsible.organization_id == Organization.id,
        )
        .outerjoin(Employee, Employee.id == OrganizationResponsible.user_id)
        .filter(
            Bid.id == bid_id,
            or_(Bid.author_id == Employee.id, Employee.username == username),
        )
    )

    access_result = await session.execute(stmt)
    accessible_bid = access_result.scalars().first()
    if accessible_bid is None:
        raise HTTPException(status_code=403, detail="Access denied")
    return accessible_bid


async def get_bid_by_id_for_user(
    session: AsyncSession, bid_id: UUID, username: str, edit_mode: bool = False
):
    bid = await get_bid_by_id(session, bid_id)
    if not edit_mode and bid.status == BidStatus.Published:
        return bid

    try:
        accessible_bid = await get_bid_for_tender_organization(
            session, bid_id, username
        )
    except HTTPException:
        accessible_bid = None

    if accessible_bid is None:
        try:
            accessible_bid = await get_bid_for_bid_organization(
                session, bid_id, username
            )
        except HTTPException:
            accessible_bid = None

    if accessible_bid is None:
        raise HTTPException(status_code=403, detail="Access denied")

    return accessible_bid


async def change_bid_status(
    session: AsyncSession, bid_id: UUID, new_status: BidStatus, username: str
):
    bid = await get_bid_by_id_for_user(session, bid_id, username, edit_mode=True)
    bid.status = new_status

    await session.commit()
    await session.refresh(bid)
    return bid


async def edit_bid(
    session: AsyncSession, bid_update: BidUpdate, bid_id: UUID, username: str
):
    bid = await get_bid_for_bid_organization(session, bid_id, username)

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
    limit: int | None = None,
    offset: int | None = None,
) -> List[Bid]:
    # Организация запрашивающего
    organization_id = await get_organization_id_by_username(session, username)

    await get_tender_by_id(session, tender_id)

    access_query = (
        select(Bid)
        .join(Tender, Tender.id == Bid.tender_id)
        .join(
            OrganizationResponsible,
            Tender.organization_id == OrganizationResponsible.organization_id,
        )
        .join(Employee, OrganizationResponsible.user_id == Employee.id)
        .filter(
            (Tender.id == tender_id)
            & (
                (Tender.organization_id == organization_id)
                | (Employee.username == username)
                | (Bid.status == BidStatus.Published)
            )
        )
        .order_by(Bid.name.asc())
        .limit(limit)
        .offset(offset)
        .distinct()
    )

    access_result = await session.execute(access_query)
    bids = access_result.scalars().all()

    if bids is None:
        raise HTTPException(status_code=403, detail="Access denied")

    return bids


async def make_feedback(
    session: AsyncSession, bid_id: UUID, bid_feedback: str, username: str
):
    bid = await get_bid_for_tender_organization(session, bid_id, username)

    new_feedback = Feedback(
        bid_id=bid_id, description=bid_feedback, creator_username=username
    )

    session.add(new_feedback)
    await session.commit()
    await session.refresh(new_feedback)
    return bid


async def get_reviews(
    session: AsyncSession,
    tender_id: UUID,
    author_username: str,
    request_username: str,
    limit: int | None,
    offset: int | None,
):
    author = await get_user_by_username(session, author_username)

    await get_tender_by_id_for_user(session, tender_id, request_username)

    stmt = (
        select(Feedback)
        .join(Bid, Bid.id == Feedback.bid_id)
        .filter(Bid.tender_id == tender_id)
        .filter(Bid.author_id == author.id)
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(stmt)
    feedbacks = result.scalars().all()

    return feedbacks


async def get_vote_by_user_id(session: AsyncSession, bid_id: UUID, user_id: UUID):
    stmt = select(Vote).filter((Vote.bid_id == bid_id) & (Vote.user_id == user_id))
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_vote(session: AsyncSession, bid_id: UUID, user_id: UUID):
    vote = await get_vote_by_user_id(session, bid_id, user_id)
    if vote is not None:
        raise HTTPException(status_code=400, detail="This user voted earlier")

    vote = Vote(bid_id=bid_id, user_id=user_id)
    session.add(vote)
    await session.commit()
    await session.refresh(vote)
    return vote


async def delete_votes(session: AsyncSession, bid_id: UUID, user_id: UUID):
    stmt = delete(Vote).filter(Vote.bid_id == bid_id)
    await session.execute(stmt)
    await session.commit()


async def submit_decision(
    session: AsyncSession, bid_id: UUID, new_desicion: BidDecision, username: str
):
    user = await get_user_by_username(session, username)
    bid = await get_bid_for_tender_organization(session, bid_id, username)

    if new_desicion == BidDecision.Approved:
        await create_vote(session, bid_id, user.id)
        bid.votes_qty += 1
        if bid.votes_qty == bid.kvorum:
            bid.decision = new_desicion
            await change_tender_status_by_id(
                session, bid.tender_id, username, TenderStatus.Closed
            )
    else:
        bid.decision = BidDecision.Rejected
        bid.status = BidStatus.Canceled
        bid.votes_qty = 0
        await delete_votes(session, bid_id, user.id)
        await change_bid_status(session, bid_id, BidStatus.Canceled, username)

    await session.commit()
    await session.refresh(bid)
    return bid


async def get_bid_history_by_id(session: AsyncSession, bid_id: UUID, version: int):
    history_stmt = select(BidHistory).filter_by(bid_id=bid_id, version=version)
    history_result = await session.execute(history_stmt)
    bid_history = history_result.scalar_one_or_none()
    if not bid_history:
        raise HTTPException(status_code=404, detail="Bid with such version not found")

    return bid_history


async def rollback(session: AsyncSession, bid_id: UUID, version: int, username: str):
    bid = await get_bid_for_bid_organization(session, bid_id, username)

    bid_history = await get_bid_history_by_id(session, bid_id, version)

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
