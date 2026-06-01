
## System Context Diagram (Level 1)

<p align="center">
  <img src="assets/System Context Diagram.drawio.svg" alt="System Context Diagram"/>
</p>

#### Context Specification

**User**: Uploads documents, validates OCR and translation results, manages terminology, and exports finalized documents.

**Document Intelligence Platform**: Processes scanned documents and PDFs using OCR, translation, terminology lookup, template reuse, and document export workflows.

**Transliteration API**: Provides transliteration for proper names, addresses, and other entities when required.

**Search Engine**: Retrieves company logos and reference images to support document template reconstruction.


## Container Diagram (Level 2)

<p align="center">
  <img src="assets/Container Diagram.drawio.svg" alt="Container Diagram"/>
</p>

#### Container Specification

**Web Interface**: User interface for document upload, OCR validation, translation review, terminology management, and document export.

**Backend Server**: Manages application workflows, document processing orchestration, storage access, template matching, and integration with external services.

**Database (Relational)**: Stores documents metadata, terminology dictionaries, translation templates, and application data.

**Message Broker**: Queues long-running document processing tasks.

**Task Queue**: Execute background jobs such as OCR, translation and substitution into the corresponding template.

**LLM Engine**: Provides local AI inference for document translation, terminology-aware processing, and template-assisted content generation.
