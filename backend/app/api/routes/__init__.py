from fastapi import APIRouter
from .employees import router as employees_router
from .departments import router as departments_router
from .timesheets import router as timesheets_router
from .leaverequests import router as leaverequests_router

api_router = APIRouter()
api_router.include_router(employees_router, tags=["employees"])
api_router.include_router(departments_router, tags=["departments"])
api_router.include_router(timesheets_router, tags=["timesheets"])
api_router.include_router(leaverequests_router, tags=["leaverequests"])
