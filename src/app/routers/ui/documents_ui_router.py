# Backend
from fastapi import APIRouter, Request

# Custom
from app.core.templates import templates
from app.dependencies import RepositoryDep
from app.utilities import build_stage_chain

router = APIRouter(
    prefix="/ui/documents",
    tags=["documents"],
)


@router.get("/table")
async def documents_table(request: Request, repository: RepositoryDep):
    documents = repository.get_documents()

    for document in documents:
        document["stage_chain"] = build_stage_chain(repository, document["document_id"])

    return templates.TemplateResponse(
        request=request,
        name="partial/document_table.html",
        context={"documents": documents},
    )
