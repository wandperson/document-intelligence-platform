# Standard
from uuid import UUID
from enum import StrEnum

# ORM
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Uuid,
    Integer,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    func,
)

# Custom
from .base_model import Base


class ProcessStage(StrEnum):
    UPLOADED = "uploaded"
    TEXT_EXTRACTED = "text_extracted"
    APPROVED_EXTRACTION = "approved_extraction"
    TEXT_TRANSLATED = "text_translated"
    APPROVED_TRANSLATION = "approved_translation"


class ProcessStatus(StrEnum):
    NOT_STARTED = "not_started"
    SUSPENDED = "suspended"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    DONE = "done"


class DocumentEvent(Base):
    __tablename__ = "document_events"

    document_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("documents.document_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    stage: Mapped[ProcessStage] = mapped_column(
        SQLEnum(ProcessStage, native_enum=False),
        primary_key=True,
        nullable=False,
    )
    status: Mapped[ProcessStatus] = mapped_column(
        SQLEnum(ProcessStatus, native_enum=False),
        nullable=False,
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class PageEvent(Base):
    __tablename__ = "page_events"

    page_id: Mapped[UUID] = mapped_column(
        Integer,
        ForeignKey("pages.page_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    stage: Mapped[ProcessStage] = mapped_column(
        SQLEnum(ProcessStage, native_enum=False),
        primary_key=True,
        nullable=False,
    )
    status: Mapped[ProcessStatus] = mapped_column(
        SQLEnum(ProcessStatus, native_enum=False),
        nullable=False,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
