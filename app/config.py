import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from asgi_logger import AccessLoggerMiddleware
from pydantic import BaseSettings

class AppSettings(BaseSettings):
    # Registrar variables de entorno de app.env
    app_token: str
    url_citas: str
    app_name: str = "Dentalink_FastAPI"
    app_version: str = "0.0.1"
    app_description: str = "API for Dentalink"

settings = AppSettings()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    middleware=[Middleware(AccessLoggerMiddleware,
                           logger=logging.getLogger("asgi_access"),
                           format="%(p)s %(h)s %(r)s %(a)s %(s)s %(L)ss")]
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.config.fileConfig('log.conf', disable_existing_loggers=True)
logging.getLogger("gunicorn.access").handler = []
logging.getLogger("uvicorn.access").handler = []

logging.info("Starting app")