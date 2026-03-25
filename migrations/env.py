import asyncio
import os
import sys

# Добавляем корень проекта в пути поиска Python
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# 1. Твои импорты
from config import settings
from database.models import Base



# Стандартный объект конфига Alembic
config = context.config

# Настройка логирования на основе файла alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Передаем метаданные моделей
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме."""
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме (асинхронно)."""
    
    # СОЗДАЕМ ENGINE НАПРЯМУЮ ИЗ SETTINGS
    connectable = create_async_engine(
        settings.database_url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())