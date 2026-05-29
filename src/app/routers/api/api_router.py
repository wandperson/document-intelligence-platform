# Standard
import base64

# Backend
from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
)
import filetype  # type: ignore

# Custom
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
async def upload_document(file: UploadFile, analyze: bool = False):
    # `content_type` in `file` can be spoofed,
    # so it's better to check the content
    # as reading first bytes from the file
    file_header = await file.read(261)
    # First 261 bytes representing the max file header is required
    kind = filetype.guess(file_header)

    if not kind or kind.mime not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    # Reset the cursor
    await file.seek(0)

    text = None

    if analyze:
        file_bytes = await file.read()
        b64_file = base64.b64encode(file_bytes).decode("utf-8")
        text = await get_text_from_image(b64_file)

    return {
        "filename": file.filename,
        "type": kind.mime,
        "extension": kind.extension,
        "text": text,
    }
