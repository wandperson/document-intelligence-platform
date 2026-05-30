# Standard
from pathlib import Path

# Backend
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()


TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )


@router.get("/documents", response_class=HTMLResponse)
def upload(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="documents.html",
    )
