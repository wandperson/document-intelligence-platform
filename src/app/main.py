# Standard
from contextlib import asynccontextmanager

# Backend
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Custom modules
from app.core.config import MAIN_DIR
from app.database import InMemoryRepo
from app.routers.api import api_router
from app.routers import root_router
from app.routers.ui import documents_ui_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = InMemoryRepo()

    app.state.database = database

    yield


app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory=MAIN_DIR / "static"))

app.include_router(api_router.router)
app.include_router(root_router.router)
app.include_router(documents_ui_router.router)
