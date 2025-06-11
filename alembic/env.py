from logging.config import fileConfig
from src.database import Base

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
def get_engine():
    return create_async_engine(
        "postgresql+asyncpg://postgres:post667@db:5432/fastapi", echo=True
    )

# Инициализация базы данных для Alembic
async def run_migrations_online():
    # Получаем асинхронный движок
    connectable = get_engine()

    # Асинхронное соединение
    async with connectable.connect() as connection:
        # Настроим контекст Alembic для асинхронного соединения
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_type=True,
            compare_server_default=True,
        )

        # Начинаем транзакцию и запускаем миграции
        async with connection.begin():
            await context.run_migrations()
