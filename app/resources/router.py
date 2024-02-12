from fastapi import APIRouter
from app.resources.dentalink import router as resources_router

router = APIRouter()
router.include_router(resources_router, prefix="/dentalink", tags=["dentalink"])