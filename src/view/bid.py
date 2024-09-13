from fastapi import APIRouter, Path, Query, status, Depends
from typing import List
from src.schemas.enums import BidDecision, BidStatus
from src.db.connection.session import get_session
from src.schemas.bid import BidCreate, BidResponse, BidUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers import bids


bid_router = APIRouter(prefix="/bids", tags=["bids"])


@bid_router.post("/new", status_code=status.HTTP_200_OK, response_model=BidResponse)
async def create_bid(bid: BidCreate, db: AsyncSession = Depends(get_session)):
    return await bids.create_bid(db, bid)


@bid_router.get("/my", status_code=status.HTTP_200_OK, response_model=List[BidResponse])
async def get_user_bids(
    limit: int | None = Query(None),
    offset: int | None = Query(None),
    username: str = Query(None),
    db: AsyncSession = Depends(get_session),
):
    return await bids.get_bids_by_user(db, limit, offset, username)


@bid_router.get(
    "/{tenderId}/list",
    status_code=status.HTTP_200_OK,
    response_model=List[BidResponse],
)
async def get_bids_by_tender(
    tenderId: str = Path(...),
    username: str = Query(...),
    limit: int | None = Query(None),
    offset: int | None = Query(None),
    db: AsyncSession = Depends(get_session),
):
    return await bids.get_bids_by_tender(db, tenderId, username, limit, offset)


@bid_router.get("/{bidId}/status", status_code=status.HTTP_200_OK)
async def get_bid_status(
    db: AsyncSession = Depends(get_session),
    bidId: str = Path(...),
    username: str = Query(...),
):
    bid = await bids.get_bid_by_id(db, bidId, username)
    return bid.status


@bid_router.put(
    "/{bidId}/status", status_code=status.HTTP_200_OK, response_model=BidResponse
)
async def change_bid_status(
    status: BidStatus,
    db: AsyncSession = Depends(get_session),
    bidId: str = Path(...),
    username: str = Query(...),
):
    bid = await bids.change_bid_status(db, bidId, status, username)
    return bid


@bid_router.patch(
    "/{bidId}/edit", status_code=status.HTTP_200_OK, response_model=BidResponse
)
async def edit_bid(
    bid: BidUpdate,
    bidId: str = Path(...),
    username: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await bids.edit_bid(db, bid, bidId, username)


@bid_router.put(
    "/{bidId}/submit_decision",
    status_code=status.HTTP_200_OK,
    response_model=BidResponse,
)
async def submit_decision(
    desicion: BidDecision,
    bidId: str,
    username: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await bids.submit_decision(db, bidId, desicion, username)


@bid_router.put(
    "/{bidId}/feedback", status_code=status.HTTP_200_OK, response_model=BidResponse
)
async def make_feedback(
    bidId: str = Path(...),
    bidFeedback: str = Query(...),
    username: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await bids.make_feedback(db, bidId, bidFeedback, username)


@bid_router.put(
    "/{bidId}/rollback/{version}",
    status_code=status.HTTP_200_OK,
    response_model=BidResponse,
)
async def rollback(
    bidId: str = Path(...),
    version: int = Path(...),
    username: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await bids.rollback(db, bidId, version, username)


@bid_router.get("/{tenderId}/reviews", status_code=status.HTTP_200_OK)
async def get_revies(
    tenderId: str = Path(...),
    authorUsername: str = Query(...),
    requestUsername: str = Query(...),
    limit: int = Query(None),
    offset: int = Query(None),
    db: AsyncSession = Depends(get_session),
):
    return await bids.get_reviews(
        db, tenderId, authorUsername, requestUsername, limit, offset
    )
