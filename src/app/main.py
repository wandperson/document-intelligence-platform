# Backend
from fastapi import FastAPI

# Custom modules
from app.routers.api import api_router
from app.routers import root_router


app = FastAPI()

app.include_router(api_router.router)
app.include_router(root_router.router)
