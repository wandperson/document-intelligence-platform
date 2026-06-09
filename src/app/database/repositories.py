# Standard
from pathlib import Path

# ORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

# Custom
from app.models.document_model import Document, DocumentAsset
from app.models.doc_event_model import (
    DocumentEvent,
    PageEvent,
    ProcessStage,
    ProcessStatus,
)
from app.models.page_model import Page, PageContent, PageStatus, VarianType


class DatabaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(self, name: str):
        document = Document(document_name=name)
        self.session.add(document)
        await self.session.flush()
        return document

    async def create_document_asset(
        self,
        document_id: str,
        content_type: str,
        file_path: Path,
    ):
        asset = DocumentAsset(
            document_id=document_id,
            content_type=content_type,
            file_name=file_path.name,
            file_path=str(file_path),
        )
        self.session.add(asset)
        await self.session.flush()
        return asset

    async def get_documents(self):
        stmt = select(Document).order_by(Document.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_document(self, document_id: str):
        document = await self.session.get(Document, document_id)
        return document

    async def get_document_assets(self, document_id: str):
        stmt = select(DocumentAsset).where(DocumentAsset.document_id == document_id)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_page(
        self,
        document_id: str,
        page_number: int,
        image_path: str,
        asset_id: int,
    ):
        page = Page(
            document_id=document_id,
            page_number=page_number,
            image_path=image_path,
            asset_id=asset_id,
        )
        self.session.add(page)
        await self.session.flush()
        return page

    async def get_pages_by_document(self, document_id: str):
        stmt = select(Page).where(Page.document_id == document_id)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_page_content(
        self,
        page_id: int,
        variant: VarianType,
        status: PageStatus,
        text: str,
    ):
        page_content = PageContent(
            page_id=page_id, variant=variant, status=status, language="xx", text=text
        )
        self.session.add(page_content)
        await self.session.flush()
        return page_content

    async def get_page_content_by_document(self, document_id: str):
        stmt = (
            select(PageContent)
            .outerjoin(Page, Page.page_id == PageContent.page_id)
            .where(Page.document_id == document_id)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()


class DatabaseEventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_document_event(
        self, document_id: str, stage: ProcessStage, status: ProcessStatus
    ) -> None:
        stmt = (
            pg_insert(DocumentEvent)
            .values(
                document_id=document_id,
                stage=stage,
                status=status,
            )
            .on_conflict_do_update(
                index_elements=[DocumentEvent.document_id, DocumentEvent.stage],
                set_={"status": status},
            )
        )
        await self.session.execute(stmt)

    async def get_document_events(self, document_id: str):
        stmt = select(DocumentEvent).where(DocumentEvent.document_id == document_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_page_event(
        self,
        page_id: int,
        stage: ProcessStage,
        status: ProcessStatus,
    ) -> PageEvent:
        page_event = PageEvent(page_id=page_id, stage=stage, status=status)
        self.session.add(page_event)
        await self.session.flush()
        return page_event
