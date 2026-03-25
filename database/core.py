from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency для получения сессии (пригодится в будущем)
async def get_session():
    async with async_session() as session:
        yield session