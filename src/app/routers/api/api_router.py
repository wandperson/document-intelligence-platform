# Standard
import base64

# Backend
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
)
import filetype  # type: ignore

# Custom
from app.schemas import SuccessResponse
from app.dependencies import RepositoryDep
from app.database import ProcessStage, ProcessStatus
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
    repository: RepositoryDep,
    files: list[UploadFile] = File(...),
):
    # `content_type` in `file` can be spoofed,
    # so it's better to check the content
    # as reading first bytes from the file
    file = files[0]
    file_header = await file.read(261)
    # First 261 bytes representing the max file header is required
    kind = filetype.guess(file_header)

    if not kind or kind.mime not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    # Reset the cursor
    await file.seek(0)

    if file.filename:
        file_bytes = await file.read()
        b64_file = base64.b64encode(file_bytes).decode("utf-8")
        repository.save_document(file.filename.split(".")[0], kind.mime, b64_file)

        import time

        # Simulate downloading a large file
        time.sleep(1.5)

    return SuccessResponse(message="Document uploaded successfully")


@router.post("/{document_id}/ocr")
async def ocr_document(
    repository: RepositoryDep,
    document_id: str,
):
    document = repository.get_document(document_id)

    repository.create_event(
        document_id,
        ProcessStage.text_extracted,
        ProcessStatus.in_progress,
    )

    text = await get_text_from_image(document["base64"])

    repository.update_document_text(document_id, text)
    repository.create_event(
        document_id,
        ProcessStage.text_extracted,
        ProcessStatus.done,
    )

    repository.create_event(
        document_id,
        ProcessStage.approved_extraction,
        ProcessStatus.pending,
    )

    return SuccessResponse(message="Extracted text successfully")
