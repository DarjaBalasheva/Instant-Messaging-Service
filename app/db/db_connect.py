from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_ASYNC
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Асинхронный sessionmaker
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
