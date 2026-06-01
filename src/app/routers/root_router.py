# Backend
from fastapi import APIRouter, Request

# Custom
from app.core.templates import templates
from app.dependencies import RepositoryDep


router = APIRouter()


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )


@router.get("/documents")
def get_documents(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="documents.html",
    )


@router.get("/documents/{document_id}")
def get_document(
    request: Request,
    document_id: str,
    repository: RepositoryDep,
):
    document = repository.get_document(document_id)
    return templates.TemplateResponse(
        request=request,
        name="document_workspace.html",
        context={"document": document},
    )
