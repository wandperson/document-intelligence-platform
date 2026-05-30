# Standard
import uuid
from enum import StrEnum


class DocumentStatus(StrEnum):
    uploaded = "uploaded"
    text_extracted = "text_extracted"
    approved = "approved"


class InMemoryRepo:
    def __init__(self):
        self.documents = []

    def save_document(self, filename, type):
        self.documents.append(
            {
                "document_id": str(uuid.uuid4().hex),
                "name": filename,
                "type": type,
                "status": DocumentStatus.uploaded,
                "content": None,
            }
        )

    def get_documents(self):
        return self.documents


def seed_db(db: InMemoryRepo):
    doc_uuid = str(uuid.uuid4().hex)
    db.documents.append(
        {
            "document_id": doc_uuid,
            "name": "first_document.jpeg",
            "type": "image/jpeg",
            "status": DocumentStatus.uploaded,
            "content": None,
        }
    )

    doc_uuid = str(uuid.uuid4().hex)
    db.documents.append(
        {
            "document_id": doc_uuid,
            "name": "first_document.jpeg",
            "type": "image/jpeg",
            "status": DocumentStatus.text_extracted,
            "content": "10 lines of text an \n and another line \n and yet another line",
        }
    )
