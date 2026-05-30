# Standard
from contextlib import asynccontextmanager

# Backend
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Custom modules
from app.core.config import MAIN_DIR
from app.database import InMemoryRepo, seed_db
from app.routers.api import api_router
from app.routers import root_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = InMemoryRepo()
    seed_db(database)

    app.state.database = database

    yield


app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory=MAIN_DIR / "static"))

app.include_router(api_router.router)
app.include_router(root_router.router)
