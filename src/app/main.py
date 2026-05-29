# Backend
from fastapi import FastAPI

# Custom modules
from app.routers.api import api_router


app = FastAPI()

app.include_router(api_router.router)
