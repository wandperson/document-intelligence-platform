# Backend
from fastapi import APIRouter, Request

# Custom
from app.core.templates import templates
from app.dependencies import SessionDep
from app.database import DatabaseRepository


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
async def get_document(
    request: Request,
    document_id: str,
    session: SessionDep,
):
    db = DatabaseRepository(session)
    document = await db.get_document(document_id)
    pages = await db.get_page_content_by_document(document_id)

    return templates.TemplateResponse(
        request=request,
        name="document_workspace.html",
        context={
            "document": document,
            "pages": pages,
        },
    )
