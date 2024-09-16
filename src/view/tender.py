from uuid import UUID
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
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    service_type: List[TenderServiceType] | None = Query(None),
    db: AsyncSession = Depends(get_session),
):
    return await tenders.get_tender_list(db, limit, offset, service_type)


@tender_router.post(
    "/new", status_code=status.HTTP_200_OK, response_model=TenderResponse
)
async def create_tender(tender: TenderCreate, db: AsyncSession = Depends(get_session)):
    return await tenders.create_tender(db, tender)


@tender_router.get(
    "/my", status_code=status.HTTP_200_OK, response_model=List[TenderResponse]
)
async def get_user_tenders(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    username: str | None = Query(None),
    db: AsyncSession = Depends(get_session),
):
    return await tenders.get_tenders_by_user(db, limit, offset, username)


@tender_router.get(
    "/{tenderId}/status", status_code=status.HTTP_200_OK, response_model=TenderStatus
)
async def get_tender_status(
    db: AsyncSession = Depends(get_session),
    tenderId: UUID = Path(...),
    username: str | None = Query("test_user"),
):
    tender = await tenders.get_tender_by_id_for_user(db, tenderId, username)
    return tender.status


@tender_router.put(
    "/{tenderId}/status", status_code=status.HTTP_200_OK, response_model=TenderResponse
)
async def change_tender_status(
    status: TenderStatus,
    db: AsyncSession = Depends(get_session),
    tenderId: UUID = Path(...),
    username: str = Query("test_user"),
):
    return await tenders.change_tender_status_by_id(db, tenderId, username, status)


@tender_router.patch(
    "/{tenderId}/edit", status_code=status.HTTP_200_OK, response_model=TenderResponse
)
async def edit_tender(
    tender: TenderUpdate,
    tenderId: UUID = Path(...),
    username: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await tenders.edit_tender(db, tender, tenderId, username)


@tender_router.put(
    "/{tenderId}/rollback/{version}",
    status_code=status.HTTP_200_OK,
    response_model=TenderResponse,
)
async def rollback(
    tenderId: UUID = Path(...),
    version: int = Path(...),
    username: str = Query(...),
    db: AsyncSession = Depends(get_session),
):
    return await tenders.rollback(db, tenderId, version, username)
