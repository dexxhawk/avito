from fastapi import APIRouter, Path, Query, status, Depends
from typing import List
from fastapi.responses import PlainTextResponse
from src.schemas.enums import TenderServiceType, TenderStatus
from src.db.connection.session import get_session
from src.schemas.bid import BidCreate
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers import bids


bid_router = APIRouter(prefix="/bids",tags=["bids"])

@bid_router.post("/new", status_code=status.HTTP_200_OK)
async def create_bid(bid: BidCreate, db: AsyncSession = Depends(get_session)):
    await bids.create_bid(db, bid)

@bid_router.get("/my", status_code=status.HTTP_200_OK)
async def get_user_bids(limit: int | None = Query(None), offset: int | None = Query(None), username: str = Query (None), db: AsyncSession = Depends(get_session)):
    return await bids.get_bids_by_user(db, limit, offset, username)

# @bid_router.get("/{bid_id}/status", status_code=status.HTTP_200_OK)
# async def get_bid_status(db: AsyncSession = Depends(get_session), bid_id: str = Path(...), username: str | None = Query('test_user')):
#     bid = await bids.get_bid_by_id(db, bid_id, username)
#     return bid.status

# @bid_router.put("/{bid_id}/status", status_code=status.HTTP_200_OK)
# async def change_bid_status(status: TenderStatus, db: AsyncSession = Depends(get_session), bid_id: str = Path(...), username: str = Query('test_user')):
#     await bids.change_bid_status_by_id(db, bid_id, username, status)

# @bid_router.patch("/{bid_id}/edit", status_code=status.HTTP_200_OK)
# async def edit_bid(bid: TenderUpdate, bid_id: str = Path(...), username: str = Query(...), db: AsyncSession = Depends(get_session)):
#     await bids.edit_bid(db, bid, bid_id, username)
