from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=10,         # Сколько держать открытых соединений
    max_overflow=20,      # Сколько можно создать сверх лимита в пике
    pool_timeout=30       # Сколько ждать свободного места в пуле
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Dependency для получения сессии (пригодится в будущем)
async def get_session():
    async with async_session() as session:
        yield session