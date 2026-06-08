# Standard
import base64

# Backend
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    Form,
    File,
)
import filetype  # type: ignore
import aiofiles  # type: ignore

# Custom
from app.core.config import UPLOAD_DIR
from app.schemas import SuccessResponse
from app.dependencies import SessionDep
from app.database import DatabaseRepository
from app.models.document_model import DocumentAsset
from app.models.doc_event_model import ProcessStage, ProcessStatus
from app.models.page_model import Page, PageStatus, VarianType
from app.services import DocumentEventService
from app.infrastructure import get_text_from_image


router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
)


ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    # "application/pdf",  # Not supported yet
}


@router.post("/upload")
async def upload_document(
    session: SessionDep,
    files: list[UploadFile] = File(...),
    document_name: str = Form(...),
):
    for file in files:
        # `content_type` in `file` can be spoofed,
        # so it's better to check the content
        # as reading first bytes from the file
        file_header = await file.read(261)
        # First 261 bytes representing the max file header is required
        kind = filetype.guess(file_header)

        if not kind or kind.mime not in ALLOWED_TYPES:
            raise HTTPException(400, "Invalid file type")

    db = DatabaseRepository(session)

    # Create a document record in the database
    doc = await db.create_document(document_name)

    for file in files:
        if not file.filename:
            raise HTTPException(400, "Missing filename")

        if not file.content_type:
            raise HTTPException(400, "Missing content type")

        # Reset the cursor
        await file.seek(0)

        file_dir = UPLOAD_DIR / str(doc.document_id)
        file_dir.mkdir(exist_ok=True)

        async with aiofiles.open(file_dir / file.filename, "wb") as out:
            while chunk := await file.read(1024 * 1024):
                await out.write(chunk)

        # Create a document asset record in the database
        await db.create_document_asset(
            document_id=doc.document_id,
            content_type=file.content_type,
            file_path=file_dir / file.filename,
        )

    db_event = DocumentEventService(session)
    await db_event.init_document_events(doc.document_id)

    await session.commit()

    return SuccessResponse(message="Document uploaded successfully")


@router.post("/{document_id}/normalize")
async def normalize_document_assets(
    session: SessionDep,
    document_id: str,
):
    db = DatabaseRepository(session)

    assets: list[DocumentAsset] = await db.get_document_assets(document_id)

    db_event = DocumentEventService(session)
    await db_event.add_document_event(
        document_id,
        ProcessStage.NORMALIZED,
        ProcessStatus.IN_PROGRESS,
    )
    await session.commit()

    for num, asset in enumerate(assets, start=1):
        if not asset.content_type.startswith("image"):
            raise (HTTPException(400, "Invalid file type"))
        await db.create_page(document_id, num, asset.file_path, asset.asset_id)

    await db_event.add_document_event(
        document_id,
        ProcessStage.NORMALIZED,
        ProcessStatus.DONE,
    )

    await session.commit()

    return SuccessResponse(message="Document normalized successfully")


@router.post("/{document_id}/ocr")
async def ocr_document(
    session: SessionDep,
    document_id: str,
):
    db = DatabaseRepository(session)

    pages: list[Page] = await db.get_pages_by_document(document_id)

    db_event = DocumentEventService(session)

    for page in pages:
        await db_event.add_page_event(
            document_id,
            page.page_id,
            ProcessStage.TEXT_EXTRACTED,
            ProcessStatus.IN_PROGRESS,
        )
        await session.commit()

        with open(page.image_path, "rb") as f:
            file_bytes = f.read()

        b64_file = base64.b64encode(file_bytes).decode("utf-8")
        text = await get_text_from_image(b64_file)

        await db.create_page_content(
            page_id=page.page_id,
            variant=VarianType.ORIGINAL,
            status=PageStatus.IN_REVIEW,
            text=text,
        )

        await db_event.add_page_event(
            document_id,
            page.page_id,
            ProcessStage.TEXT_EXTRACTED,
            ProcessStatus.DONE,
        )

        await session.commit()

    return SuccessResponse(message="Text extracted successfully")


# @router.post("/ocr-file")
# async def ocr_file(
#     session: SessionDep,
#     file: UploadFile = File(...),
# ):
#     # `content_type` in `file` can be spoofed,
#     # so it's better to check the content
#     # as reading first bytes from the file
#     file_header = await file.read(261)
#     # First 261 bytes representing the max file header is required
#     kind = filetype.guess(file_header)

#     if not kind or kind.mime not in ALLOWED_TYPES:
#         raise HTTPException(400, "Invalid file type")

#     # Reset the cursor
#     await file.seek(0)

#     file_bytes = await file.read()
#     b64_file = base64.b64encode(file_bytes).decode("utf-8")

#     text = await get_text_from_image(b64_file)

#     return {
#         "text": text,
#     }
