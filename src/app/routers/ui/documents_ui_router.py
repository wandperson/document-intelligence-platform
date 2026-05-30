# Backend
from fastapi import APIRouter, Request

# Custom
from app.core.templates import templates
from app.dependencies import RepositoryDep


router = APIRouter(
    prefix="/ui/documents",
    tags=["documents"],
)


@router.get("/table")
async def documents_table(request: Request, repository: RepositoryDep):
    documents = repository.get_documents()

    return templates.TemplateResponse(
        request=request,
        name="partial/document_table.html",
        context={"documents": documents},
    )
