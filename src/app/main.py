# Standard
from contextlib import asynccontextmanager

# Backend
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Custom modules
from app.core.config import MAIN_DIR, get_settings
from app.database import create_engine, create_session_maker

from app.routers.api import document_api_router
from app.routers import app_router
from app.routers.ui import document_ui_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine(get_settings().postgres_url)
    session_maker = create_session_maker(engine)

    app.state.engine = engine
    app.state.session_maker = session_maker

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory=MAIN_DIR / "static"))

app.include_router(document_api_router.router)
app.include_router(app_router.router)
app.include_router(document_ui_router.router)
