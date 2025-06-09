from fastapi import APIRouter
from src.api.tasks import router as tasks_router
from src.api.users import router as users_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(tasks_router)