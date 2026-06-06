# Standard
from uuid import uuid4, UUID

# ORM
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Uuid,
    Integer,
    DateTime,
    String,
    ForeignKey,
    func,
)

# Custom
from .base_model import Base


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    document_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class DocumentAsset(Base):
    __tablename__ = "document_assets"

    asset_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    document_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("documents.document_id", ondelete="CASCADE"),
        nullable=False,
    )
    source_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
