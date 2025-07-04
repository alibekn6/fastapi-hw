from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
