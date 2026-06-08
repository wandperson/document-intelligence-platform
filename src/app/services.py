# Validation
from pydantic import BaseModel

# Custom
from app.database import DatabaseEventRepository
from app.models.doc_event_model import (
    ProcessStage,
    ProcessStatus,
    DocumentEvent,
)


class StageMeta(BaseModel):
    label: str
    tooltip: str


class StatusMeta(BaseModel):
    color: str
    tooltip: str


STAGES: dict[ProcessStage, StageMeta] = {
    ProcessStage.NORMALIZED: StageMeta(
        label="N",
        tooltip="Normalized",
    ),
    ProcessStage.TEXT_EXTRACTED: StageMeta(
        label="E",
        tooltip="Extracted Text",
    ),
    ProcessStage.APPROVED_EXTRACTION: StageMeta(
        label="A",
        tooltip="Approved Extraction",
    ),
    ProcessStage.TEXT_TRANSLATED: StageMeta(
        label="T",
        tooltip="Translated",
    ),
    ProcessStage.APPROVED_TRANSLATION: StageMeta(
        label="A",
        tooltip="Approved Translation",
    ),
}


STAGE_ORDER: list[ProcessStage] = [
    ProcessStage.NORMALIZED,
    ProcessStage.TEXT_EXTRACTED,
    ProcessStage.APPROVED_EXTRACTION,
    ProcessStage.TEXT_TRANSLATED,
    ProcessStage.APPROVED_TRANSLATION,
]


STATUSES: dict[ProcessStatus, StatusMeta] = {
    ProcessStatus.NOT_STARTED: StatusMeta(
        color="bg-gray-300",
        tooltip="Not Started",
    ),
    ProcessStatus.SUSPENDED: StatusMeta(
        color="bg-yellow-500",
        tooltip="Suspended",
    ),
    ProcessStatus.PENDING: StatusMeta(
        color="bg-yellow-500",
        tooltip="Pending",
    ),
    ProcessStatus.IN_PROGRESS: StatusMeta(
        color="bg-blue-500",
        tooltip="In Progress",
    ),
    ProcessStatus.FAILED: StatusMeta(
        color="bg-red-500",
        tooltip="Failed",
    ),
    ProcessStatus.DONE: StatusMeta(
        color="bg-green-500",
        tooltip="Done",
    ),
}


class DocumentProcessService:
    @staticmethod
    async def build_stage_chain(session, document_id: str):
        db = DatabaseEventRepository(session)
        doc_events = await db.get_document_events(document_id)
        events_by_stage = {event.stage: event for event in doc_events}
        # Resolve stage chain
        chain = []

        for stage in STAGE_ORDER:
            doc_event: DocumentEvent | None = events_by_stage.get(stage)

            # Skip if stage is not found in events table
            if not doc_event:
                continue

            currunt_stage = STAGES[doc_event.stage]
            current_status = STATUSES[doc_event.status]
            chain.append(
                {
                    "stage_tooltip": currunt_stage.tooltip,
                    "label": currunt_stage.label,
                    "status_tooltip": current_status.tooltip,
                    "color": current_status.color,
                }
            )

        return chain


class DocumentEventService:
    def __init__(self, session):
        self.db_event = DatabaseEventRepository(session)

    async def init_document_events(self, document_id: str) -> None:
        for stage in ProcessStage:
            await self.db_event.update_document_event(
                document_id=document_id,
                stage=stage,
                status=ProcessStatus.NOT_STARTED,
            )

    async def add_document_event(
        self,
        document_id: str,
        stage: ProcessStage,
        status: ProcessStatus,
    ):
        await self.db_event.update_document_event(
            document_id=document_id,
            stage=stage,
            status=status,
        )

    async def add_page_event(
        self,
        document_id: str,
        page_id: int,
        stage: ProcessStage,
        status: ProcessStatus,
    ):
        await self.db_event.create_page_event(
            page_id=page_id, stage=stage, status=status
        )
        await self.db_event.update_document_event(
            document_id=document_id,
            stage=stage,
            status=status,
        )
