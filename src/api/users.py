from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from src.models.users import UserModel
from src.schemas.users import UserCreateSchema, UserGetSchema, UserLoginSchema
from src.api.dependencies import SessionDep
from src.utils.auth import hash_password, verify_password
from src.utils.jwt import create_access_token
from src.database import engine, Base
from src.utils.jwt import get_current_user


router = APIRouter(prefix="/auth", tags=["Tasks"])

@router.post("/setup")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@router.post("/register", response_model=UserGetSchema)
async def register(user: UserCreateSchema, session: SessionDep):
    result = await session.execute(
        select(UserModel).where(UserModel.username == user.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post("/login")
async def login(user: UserLoginSchema, session: SessionDep):
    result = await session.execute(
        select(UserModel).where(UserModel.username == user.username)
    )
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserGetSchema)
async def me(current_user: UserModel = Depends(get_current_user)):
    return current_user
