# Document Intelligence Platform

## Overview

This project is a document processing system designed to handle scanned documents and images, extract text, translate it between languages, and generate structured output documents.

It is focused on building a full document processing pipeline, including:
- OCR text and layout extraction from images and PDFs
- Multilingual translation (English, Ukrainian, Japanese)
- Result document generation in DOCX / PDF formats


## Architecture

See detailed architecture documentation:
- [Architecture Documentation](docs/ARCHITECTURE.md)


## Key Features Scope

#### Core Document Pipeline

- [x] Upload documents as images
- [ ] Upload documents as PDF
- [x] Drag-and-drop upload
- [ ] Bulk upload of documents
- [ ] OCR processing autostart on upload
- [x] Text extraction from documents
- [ ] Advanced text extraction with layout analysis
- [ ] OCR processing with structure detection (blocks / paragraphs / tables)

#### Document Management Layer

- [x] Document processing state machine (stage-based lifecycle tracking)
- [ ] Search for documents in the system
- [ ] Tags feature implementation for document
- [ ] Documents versioning (on each stage of processing)
- [ ] Documents user correction and user review (on each stage of processing)
- [ ] Documents comparison (diff and translation)

#### Translation & Language Processing

- [ ] Translation of extracted text
- [ ] Transliteration of extracted text
- [x] Integration of local LLM engine
- [ ] Terminology glossaries for repeated terms
- [ ] Automated creation of glossaries after user corrections

#### Knowledge & Reuse Layer

- [ ] Template creation from document to use for in future processing of similar documents
- [ ] Document similarity detection via fingerprints to reduce processing time
- [ ] Context-aware translation using stored terminology and history

#### Output Generation

- [ ] Export to DOCX or PDF with similar layout as original document (tables, spacing, structure)
- [ ] Image and logo enrichment based on document content

#### Infrastructure & System Design

- [x] Connect database
- [ ] Connect message broker and task queue
- [ ] Docker deployment
- [ ] GitHub Actions for DockerHub deployment
- [ ] Infrastructure repository for production server deployment


## Status

Functional MVP in active development.
