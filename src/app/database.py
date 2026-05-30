# Standard
import datetime as dt
import uuid
from enum import StrEnum


class ProcessStage(StrEnum):
    uploaded = "uploaded"
    text_extracted = "text_extracted"
    approved_extraction = "approved_extraction"
    text_translated = "text_translated"
    approved_translation = "approved_translation"


class ProcessStatus(StrEnum):
    suspended = "suspended"
    pending = "pending"
    in_progress = "in_progress"
    failed = "failed"
    done = "done"


class InMemoryRepo:
    def __init__(self):
        self.documents = []
        self.document_events = []

    def save_document(self, filename, type):
        doc_uuid = str(uuid.uuid4().hex)
        document = {
            "document_id": doc_uuid,
            "name": filename,
            "type": type,
            "created_at": dt.datetime.now(),
            "content": None,
        }
        self.documents.append(document)
        event = {
            "document_id": doc_uuid,
            "stage": ProcessStage.uploaded,
            "status": ProcessStatus.done,
            "created_at": dt.datetime.now(),
        }
        self.document_events.append(event)
        return document

    def create_event(self, document_id, stage, status):
        event = {
            "document_id": document_id,
            "stage": stage,
            "status": status,
            "created_at": dt.datetime.now(),
        }
        self.document_events.append(event)
        return event

    def get_documents(self):
        return sorted(self.documents, key=lambda x: x["created_at"], reverse=True)

    def get_document_events(self, document_id: str):
        return [e for e in self.document_events if e["document_id"] == document_id]


def seed_db(db: InMemoryRepo):
    doc_uuid = str(uuid.uuid4().hex)
    db.documents.append(
        {
            "document_id": doc_uuid,
            "name": "first_document",
            "type": "image/jpeg",
            "created_at": dt.datetime.now() - dt.timedelta(hours=1, minutes=14),
            "content": None,
        }
    )

    db.create_event(doc_uuid, ProcessStage.uploaded, ProcessStatus.done)

    doc_uuid = str(uuid.uuid4().hex)
    db.documents.append(
        {
            "document_id": doc_uuid,
            "name": "some_new_doc",
            "type": "image/jpeg",
            "created_at": dt.datetime.now() - dt.timedelta(minutes=37),
            "content": "10 lines of text an \n and another line \n and yet another line",
        }
    )
    db.create_event(doc_uuid, ProcessStage.uploaded, ProcessStatus.done)
    db.create_event(doc_uuid, ProcessStage.text_extracted, ProcessStatus.done)
    db.create_event(doc_uuid, ProcessStage.approved_extraction, ProcessStatus.pending)
