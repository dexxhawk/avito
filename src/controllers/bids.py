from http.client import HTTPException
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete, join, or_, select
from src.schemas.enums import TenderServiceType, TenderStatus
from src.db.models.models import Bid, Employee, Organization, OrganizationResponsible, Tender
from src.schemas.bid import BidCreate
from src.schemas.response import ErrorResponseBase


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
            detail="Не удалось создать данное предложение"
        )
    return new_bid


# async def get_bid_list(session: AsyncSession, limit: int, offset: int, service_type: List[TenderServiceType] | None) -> List[Tender]:
#     query = select(Tender).limit(limit).offset(offset)
#     if service_type:
#         query = query.filter(Tender.service_type.in_(service_type))
#     result = await session.execute(query)
#     return result.scalars().all()

# # async def get_user_bids(session: AsyncSession):
# #     query = select(Tender).
# #     result = await session.execute(query)
# #     return result.scalars().all()


# async def get_bid(session: AsyncSession, bid_id: int) -> Tender:
#     query = select(Tender).filter(Tender.id == bid_id)
#     result = await session.execute(query)
#     return result.scalars().first()

# # async def change_bid_status(session: AsyncSession, bid_id: int, status: TenderStatus):
# #     query = select(Tender).filter(Tender.id == bid_id)
# #     result = await session.execute(query)
# #     bid = result.scalars().first()
# #     setattr(bid, status, status)


async def get_bids_by_user(session: AsyncSession, limit: int | None, offset: int | None, username: str):
    query = (
        select(Bid)
        .select_from(
            join(
                Bid,
                Tender,
                Bid.tender_id == Tender.id
            ).join(
                Organization,
                Tender.organization_id == Organization.id
            ).join(
                OrganizationResponsible,
                Organization.id == OrganizationResponsible.organization_id
            ).join(
                Employee,
                OrganizationResponsible.user_id == Employee.id
            )
        )
        .filter(Bid.creator_username == username)
        .limit(limit)
        .offset(offset)
    )
    
    result = await session.execute(query)
    bids = result.scalars().all()
    
    return bids


# async def get_bid_by_id(
#     session: AsyncSession, bid_id: str, username: Optional[str] = None
# ):
#     query = select(Tender).where(Tender.id == bid_id)
    
#     result = await session.execute(query)
#     bid = result.scalars().first()

#     if not bid:
#         raise HTTPException(status_code=404, detail="Tender not found")
    
#     if bid.status == "Published":
#             return bid
#     if username is None:
#         raise HTTPException(status_code=403, detail="Access denied")

#     # Проверяем, связан ли пользователь с организацией
#     org_query = (
#         select(Employee)
#         .join(OrganizationResponsible, Employee.id == OrganizationResponsible.user_id)
#         .where(Employee.username == username)
#         .where(OrganizationResponsible.organization_id == bid.organization_id)
#     )
#     user_in_org = await session.execute(org_query)
#     user = user_in_org.scalars().first()

#     if user:
#         return bid
#     else:
#         raise HTTPException(status_code=403, detail="Access denied")


# async def change_bid_status_by_id(
#     session: AsyncSession, bid_id: str, username: str, new_status: TenderStatus
# ):
#     query = select(Tender).where(Tender.id == bid_id)
#     result = await session.execute(query)
#     bid = result.scalars().first()

#     if not bid:
#         raise HTTPException(status_code=404, detail="Tender not found")

#     if username is None:
#         raise HTTPException(status_code=403, detail="Username not specified")

#     # Проверяем, связан ли пользователь с организацией
#     org_query = (
#         select(Employee)
#         .join(OrganizationResponsible, Employee.id == OrganizationResponsible.user_id)
#         .where(Employee.username == username)
#         .where(OrganizationResponsible.organization_id == bid.organization_id)
#     )
#     user_in_org = await session.execute(org_query)
#     user = user_in_org.scalars().first()

#     if user:
#         bid.status = new_status
#         try:
#             await session.commit()
#             await session.refresh(bid)
#             return bid
#         except IntegrityError:
#             await session.rollback()
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error changing bid status")

#     else:
#         raise HTTPException(status_code=403, detail="Access denied")
    

# async def edit_bid(
#     session: AsyncSession, bid_update: TenderUpdate, bid_id: str, username: str
# ):
#     query = select(Tender).where(Tender.id == bid_id)
#     result = await session.execute(query)
#     bid = result.scalars().first()

#     if not bid:
#         raise HTTPException(status_code=404, detail="Tender not found")

#     if username is None:
#         raise HTTPException(status_code=403, detail="Username not specified")

#     # Проверяем, связан ли пользователь с организацией
#     org_query = (
#         select(Employee)
#         .join(OrganizationResponsible, Employee.id == OrganizationResponsible.user_id)
#         .where(Employee.username == username)
#         .where(OrganizationResponsible.organization_id == bid.organization_id)
#     )
#     user_in_org = await session.execute(org_query)
#     user = user_in_org.scalars().first()

#     if user:
#         for key, val in bid_update.model_dump(exclude_unset=True).items():
#             setattr(bid, key, val)
#         try:
#             await session.commit()
#             await session.refresh(bid)
#             return bid
#         except IntegrityError:
#             await session.rollback()
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error changing bid status")

#     else:
#         raise HTTPException(status_code=403, detail="Access denied")