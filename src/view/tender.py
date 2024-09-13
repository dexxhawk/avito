from fastapi import APIRouter, Query, status, Depends
from typing import List
from fastapi.responses import PlainTextResponse
from src.schemas.enums import TenderServiceType
from src.db.connection.session import get_session
from src.schemas.tender import TenderCreate, TenderResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers import tenders


tender_router = APIRouter(prefix="/tenders",tags=["tender"])

@tender_router.get("/", status_code=status.HTTP_200_OK, response_model=List[TenderResponse])
async def get_tenders(limit: int, offset: int, service_type: List[TenderServiceType] | None = Query(None), db: AsyncSession = Depends(get_session)):
    return await tenders.get_tender_list(db, limit, offset, service_type)


@tender_router.post("/new", status_code=status.HTTP_200_OK)
async def create_tender(tender: TenderCreate, db: AsyncSession = Depends(get_session)):
    await tenders.create_tender(db, tender)

@tender_router.post("/my", status_code=status.HTTP_200_OK)
async def get_user_tenders(limit: int, offset: int, username: str, db: AsyncSession = Depends(get_session)):
    return await tenders.get_tenders_by_user(db, limit, offset, username)
