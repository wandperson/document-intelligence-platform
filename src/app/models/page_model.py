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
    SmallInteger,
    DateTime,
    ForeignKey,
    String,
    Text,
    Enum as SQLEnum,
    UniqueConstraint,
    func,
)

# Custom
from .base_model import Base


class PageStatus(StrEnum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"


class VarianType(StrEnum):
    ORIGINAL = "original"
    TRANSLATED = "translated"


class Page(Base):
    __tablename__ = "pages"

    page_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    document_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("documents.document_id", ondelete="CASCADE"),
        nullable=False,
    )
    page_number: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    image_path: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )
    asset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("document_assets.asset_id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "page_number",
        ),
    )


class PageContent(Base):
    __tablename__ = "page_contents"

    page_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("pages.page_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    variant: Mapped[VarianType] = mapped_column(
        SQLEnum(VarianType, native_enum=False),
        nullable=False,
    )
    status: Mapped[PageStatus] = mapped_column(
        SQLEnum(PageStatus, native_enum=False),
        nullable=False,
    )
    language: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
