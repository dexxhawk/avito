from fastapi import APIRouter, Path, Query, status, Depends
from typing import List
from fastapi.responses import PlainTextResponse
from src.schemas.tender import TenderUpdate
from src.schemas.enums import BidDecision, BidStatus, TenderServiceType, TenderStatus
from src.db.connection.session import get_session
from src.schemas.bid import BidCreate, BidResponse, BidUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers import bids


bid_router = APIRouter(prefix="/bids",tags=["bids"])

@bid_router.post("/new", status_code=status.HTTP_200_OK, response_model=BidResponse)
async def create_bid(bid: BidCreate, db: AsyncSession = Depends(get_session)):
    return await bids.create_bid(db, bid)

@bid_router.get("/my", status_code=status.HTTP_200_OK, response_model=List[BidResponse])
async def get_user_bids(limit: int | None = Query(None), offset: int | None = Query(None), username: str = Query (None), db: AsyncSession = Depends(get_session)):
    return await bids.get_bids_by_user(db, limit, offset, username)

@bid_router.get("/{tender_id}/list", status_code=status.HTTP_200_OK, response_model=List[BidResponse])
async def get_bids_by_tender(tender_id: str = Path(...), username: str = Query(...), limit: int | None = Query(None), offset: int | None = Query(None), db: AsyncSession = Depends(get_session)):
    return await bids.get_bids_by_tender(db, tender_id, username, limit, offset)

@bid_router.get("/{bid_id}/status", status_code=status.HTTP_200_OK)
async def get_bid_status(db: AsyncSession = Depends(get_session), bid_id: str = Path(...), username: str  = Query(...)):
    bid = await bids.get_bid_by_id(db, bid_id, username)
    return bid.status

@bid_router.put("/{bid_id}/status", status_code=status.HTTP_200_OK, response_model=BidResponse)
async def change_bid_status(status: BidStatus, db: AsyncSession = Depends(get_session), bid_id: str = Path(...), username: str  = Query(...)):
    bid = await bids.change_bid_status(db, bid_id, status, username)
    return bid

@bid_router.patch("/{bid_id}/edit", status_code=status.HTTP_200_OK, response_model=BidResponse)
async def edit_bid(bid: BidUpdate, bid_id: str = Path(...), username: str = Query(...), db: AsyncSession = Depends(get_session)):
    return await bids.edit_bid(db, bid, bid_id, username)

@bid_router.put("/{bid_id}/submit_decision", status_code=status.HTTP_200_OK, response_model=BidResponse)
async def submit_decision(desicion: BidDecision, bid_id: str, username: str = Query(...), db: AsyncSession = Depends(get_session)):
    return await bids.submit_decision(db, bid_id, desicion, username)

@bid_router.put("/{bid_id}/feedback", status_code=status.HTTP_200_OK, response_model=BidResponse)
async def make_feedback(bid_id: str = Path(...), bid_feedback: str = Query(...), username: str = Query(...), db: AsyncSession = Depends(get_session)):
    return await bids.make_feedback(db, bid_id, bid_feedback, username)

@bid_router.put("/{bid_id}/rollback/{version}", status_code=status.HTTP_200_OK, response_model=BidResponse)
async def rollback(bid_id: str = Path(...), version: int = Path(...), username: str = Query(...), db: AsyncSession = Depends(get_session)):
    return await bids.rollback(db, bid_id, version, username)

@bid_router.get("/{tender_id}/reviews", status_code=status.HTTP_200_OK)
async def get_revies(tender_id: str = Path(...), author_username: str = Query(...), request_username: str = Query(...), limit: int = Query(None), offset: int = Query(None), db: AsyncSession = Depends(get_session)):
    return await bids.get_reviews(db, tender_id, author_username, request_username, limit, offset)  
