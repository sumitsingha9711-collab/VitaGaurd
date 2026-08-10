from fastapi import APIRouter
from app.api.routes.scan import router as scan_router
from app.api.routes import auth

api_router = APIRouter()

api_router.include_router(scan_router)
api_router.include_router(auth.router)