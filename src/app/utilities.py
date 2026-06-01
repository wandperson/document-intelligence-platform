# Standard
from typing import Any

# Custom
from app.database import InMemoryRepo, ProcessStage, ProcessStatus


STAGE_FLOW = [
    ProcessStage.uploaded,
    ProcessStage.text_extracted,
    ProcessStage.approved_extraction,
    ProcessStage.text_translated,
    ProcessStage.approved_translation,
]

STAGE_LABEL = {
    ProcessStage.uploaded: "U",
    ProcessStage.text_extracted: "E",
    ProcessStage.approved_extraction: "A",
    ProcessStage.text_translated: "T",
    ProcessStage.approved_translation: "A",
}

STAGE_TOOLTIP = {
    ProcessStage.uploaded: "Upload",
    ProcessStage.text_extracted: "Extracted Text",
    ProcessStage.approved_extraction: "Approved Extraction",
    ProcessStage.text_translated: "Translated",
    ProcessStage.approved_translation: "Approved Translation",
}

STATUS_COLOR = {
    "not_started": "bg-gray-300",
    ProcessStatus.suspended: "bg-yellow-500",
    ProcessStatus.pending: "bg-yellow-500",
    ProcessStatus.in_progress: "bg-blue-500",
    ProcessStatus.failed: "bg-red-500",
    ProcessStatus.done: "bg-green-500",
}

STATUS_TOOLTIP = {
    "not_started": "Not Started",
    ProcessStatus.suspended: "Suspended",
    ProcessStatus.pending: "Pending",
    ProcessStatus.in_progress: "In Progress",
    ProcessStatus.failed: "Failed",
    ProcessStatus.done: "Done",
}


def build_stage_chain(database: InMemoryRepo, document_id: str):
    events = database.get_document_events(document_id)

    # Get latest event
    latest_by_stage: dict[str, Any] = {}

    for e in events:
        stage = e["stage"]

        prev = latest_by_stage.get(stage)

        if prev is None or e["created_at"] > prev["created_at"]:
            latest_by_stage[stage] = e

    # Resolve stage chain
    chain = []

    for stage in STAGE_FLOW:
        event = latest_by_stage.get(stage)

        if event is None:
            status = "not_started"
            color = "bg-gray-300"
        else:
            status = event["status"]
            color = STATUS_COLOR.get(status, "bg-gray-300")

        chain.append(
            {
                "stage_tooltip": STAGE_TOOLTIP.get(stage, stage),
                "label": STAGE_LABEL[stage],
                "status_tooltip": STATUS_TOOLTIP.get(status, status),
                "color": color,
            }
        )

    return chain
