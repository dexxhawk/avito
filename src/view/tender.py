from fastapi import APIRouter, Path, Query, status, Depends
from typing import List
from src.schemas.enums import TenderServiceType, TenderStatus
from src.db.connection.session import get_session
from src.schemas.tender import TenderCreate, TenderResponse, TenderUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers import tenders


tender_router = APIRouter(prefix="/tenders", tags=["tender"])


@tender_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[TenderResponse]
)
async def get_tenders(
    limit: int,
    offset: int,
    service_type: List[TenderServiceType] | None = Query(None),
    db: AsyncSession = Depends(get_session),
):
    return await tenders.get_tender_list(db, limit, offset, service_type)


@tender_router.post("/new", status_code=status.HTTP_200_OK)
async def create_tender(tender: TenderCreate, db: AsyncSession = Depends(get_session)):
    return await tenders.create_tender(db, tender)


@tender_router.get("/my", status_code=status.HTTP_200_OK)
async def get_user_tenders(
    limit: int, offset: int, username: str, db: AsyncSession = Depends(get_session)
):
    return await tenders.get_tenders_by_user(db, limit, offset, username)


@tender_router.get("/{tender_id}/status", status_code=status.HTTP_200_OK)
async def get_tender_status(
    db: AsyncSession = Depends(get_session),
    tender_id: str = Path(...),
    username: str | None = Query("test_user"),
):
    tender = await tenders.get_tender_by_id(db, tender_id, username)
    return tender.status


@tender_router.put("/{tender_id}/status", status_code=status.HTTP_200_OK)
async def change_tender_status(
    status: TenderStatus,
    db: AsyncSession = Depends(get_session),
    tender_id: str = Path(...),
    username: str = Query("test_user"),
):
    return await tenders.change_tender_status_by_id(db, tender_id, username, status)


@tender_router.patch("/{tender_id}/edit", status_code=status.HTTP_200_OK)
async def edit_tender(
    tender: TenderUpdate,
    tender_id: str = Path(...),
    username: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await tenders.edit_tender(db, tender, tender_id, username)


@tender_router.put(
    "/{tender_id}/rollback/{version}",
    status_code=status.HTTP_200_OK,
    response_model=TenderResponse,
)
async def rollback(
    tender_id: str = Path(...),
    version: int = Path(...),
    username: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await tenders.rollback(db, tender_id, version, username)
