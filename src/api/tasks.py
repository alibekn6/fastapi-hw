from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.models.task import TaskModel
from src.schemas.task import TaskCreateSchema, TaskGetSchema
from src.utils.jwt import get_current_user
from src.database import get_session
from src.models.users import UserModel

router = APIRouter(prefix="/tasks", tags=["Tasks"])

CurrentUser = Depends(get_current_user)
DBSession = Depends(get_session)


@router.post("/users", response_model=TaskGetSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreateSchema,
    user: UserModel = CurrentUser,
    session: AsyncSession = DBSession
):
    task = TaskModel(
        title=data.title,
        description=data.description,
        user_id=user.id
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.get("/", response_model=list[TaskGetSchema])
async def read_tasks(
    user: UserModel = CurrentUser,
    session: AsyncSession = DBSession
):
    result = await session.execute(
        select(TaskModel).where(TaskModel.user_id == user.id)
    )
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskGetSchema)
async def read_task(
    task_id: int,
    user: UserModel = CurrentUser,
    session: AsyncSession = DBSession
):
    result = await session.execute(
        select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.user_id == user.id
        )
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskGetSchema)
async def update_task(
    task_id: int,
    data: TaskCreateSchema,
    user: UserModel = CurrentUser,
    session: AsyncSession = DBSession
):
    # проверяем, что задача есть и принадлежит текущему юзеру
    result = await session.execute(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.execute(
        update(TaskModel)
        .where(TaskModel.id == task_id)
        .values(title=data.title, description=data.description)
    )
    await session.commit()
    await session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user: UserModel = CurrentUser,
    session: AsyncSession = DBSession
):
    result = await session.execute(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == user.id)
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.execute(delete(TaskModel).where(TaskModel.id == task_id))
    await session.commit()
    return None
