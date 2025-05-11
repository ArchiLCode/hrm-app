from fastapi import APIRouter

from app.api.routes import login, private, users, utils
from app.api.routes import employees, departments, timesheets, leaverequests
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(employees.router)
api_router.include_router(departments.router)
api_router.include_router(timesheets.router)
api_router.include_router(leaverequests.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
