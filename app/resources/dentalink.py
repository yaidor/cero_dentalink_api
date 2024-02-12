from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime

router = APIRouter(
    tags=["dentalink"],
    responses={404: {"description": "Not found"}},
)

@router.get("/ping")
async def ping():
    return {"ping": "pong"}