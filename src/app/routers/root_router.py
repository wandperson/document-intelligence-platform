# Backend
from fastapi import APIRouter, Request

# Custom
from app.core.templates import templates


router = APIRouter()


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )


@router.get("/documents")
def upload(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="documents.html",
    )
