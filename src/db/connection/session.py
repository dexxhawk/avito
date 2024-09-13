from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import get_settings


engine = create_async_engine(
            get_settings().database_uri,
            echo=True,
            future=True,
        )

async def get_session() -> AsyncSession:
    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session