# Backend
from fastapi import APIRouter, Request

# Custom
from app.core.templates import templates
from app.dependencies import SessionDep
from app.database import DatabaseRepository
from app.services import DocumentProcessService

router = APIRouter(
    prefix="/ui/documents",
    tags=["documents"],
)


@router.get("/table")
async def documents_table(
    request: Request,
    session: SessionDep,
):
    db = DatabaseRepository(session)

    documents = await db.get_documents()

    for document in documents:
        document.stage_chain = await DocumentProcessService.build_stage_chain(
            session,
            document.document_id,
        )
        pages_count = len(await db.get_pages_by_document(document.document_id))
        document.pages = "" if pages_count == 0 else str(pages_count)

    return templates.TemplateResponse(
        request=request,
        name="partial/document_table.html",
        context={"documents": documents},
    )
