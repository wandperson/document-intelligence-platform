# Standard
import datetime as dt
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
        document = {
            "document_id": str(uuid.uuid4().hex),
            "name": filename,
            "type": type,
            "created_at": dt.datetime.now(),
            "status": DocumentStatus.uploaded,
            "content": None,
        }
        self.documents.append(document)
        return document

    def get_documents(self):
        return sorted(self.documents, key=lambda x: x["created_at"], reverse=True)


def seed_db(db: InMemoryRepo):
    doc_uuid = str(uuid.uuid4().hex)
    db.documents.append(
        {
            "document_id": doc_uuid,
            "name": "first_document",
            "type": "image/jpeg",
            "created_at": dt.datetime.now() - dt.timedelta(hours=1, minutes=14),
            "status": DocumentStatus.uploaded,
            "content": None,
        }
    )

    doc_uuid = str(uuid.uuid4().hex)
    db.documents.append(
        {
            "document_id": doc_uuid,
            "name": "some_new_doc",
            "type": "image/jpeg",
            "created_at": dt.datetime.now() - dt.timedelta(minutes=37),
            "status": DocumentStatus.text_extracted,
            "content": "10 lines of text an \n and another line \n and yet another line",
        }
    )
