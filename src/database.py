from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine: AsyncEngine = create_async_engine("postgresql+asyncpg://postgres:post667@localhost:5432/fastapi", echo=True)

new_async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_async_session() as session:
        yield session

class Base(DeclarativeBase):
    pass
