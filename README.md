# AI Invoice Intelligence

An AI-powered financial document processing system for extracting,
validating, storing, detecting duplicates, and semantically searching
invoice data.

> **Project status:** Work in Progress\
> This repository is being developed incrementally. Some components are
> implemented, while the RAG pipeline and later application layers are
> still under development.

## Overview

AI Invoice Intelligence is a document-processing project designed to
turn unstructured invoices (PDFs and images) into structured, validated,
and searchable financial records.

The intended workflow is:

1.  Ingest invoice documents in PDF or image format.
2.  Extract embedded PDF text and preprocess images.
3.  Apply OCR when a document does not contain usable text.
4.  Extract invoice fields into structured data.
5.  Validate extracted data with Pydantic and financial business rules.
6.  Store invoice records in SQLite.
7.  Detect exact, normalized, and potential duplicate invoices.
8.  Create semantic embeddings and index invoice content in Qdrant.
9.  Retrieve relevant invoices using natural-language queries.
10. Expose the workflow through an API and a user interface.

## Key Features

-   **Document ingestion:** PDF and common image formats.
-   **PDF text extraction:** Extract text from text-based PDF files.
-   **Image preprocessing:** Grayscale conversion, blur checks, and
    thresholding with OpenCV.
-   **Structured data validation:** Pydantic schemas for invoice fields.
-   **Financial validation:** Compare subtotal, VAT, and total using
    decimal arithmetic and a configurable tolerance.
-   **Relational storage:** SQLite database managed through SQLAlchemy.
-   **Duplicate detection:**
    -   Exact duplicate checks.
    -   Normalized invoice-number and supplier checks.
    -   Potential duplicate warnings based on supplier, date, amount,
        and currency.
-   **Semantic search:** Qdrant vector search using FastEmbed.
-   **Separation of concerns:** SQLite is the source of truth for
    invoice records; Qdrant is used as a semantic-search index.

## Technology Stack

  Area                      Technologies
  ------------------------- ---------------------------------
  Language                  Python
  API foundation            FastAPI
  Data validation           Pydantic
  Relational database       SQLite
  ORM                       SQLAlchemy
  Vector database           Qdrant
  Embeddings                FastEmbed
  PDF processing            PyMuPDF
  Image processing          Pillow, OpenCV, NumPy
  Configuration             python-dotenv
  Development environment   Python virtual environment, Git

## Architecture

``` text
                 +----------------------+
                 |   PDF / Image Files  |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Document Processing  |
                 | PDF Text / Images    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |    OCR (planned /    |
                 |   integration work) |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |  LLM Data Extraction |
                 |   (integration work) |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Pydantic Validation  |
                 | Financial Validation |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   SQLite + SQLAlchemy|
                 |  Source of Truth     |
                 +----------+-----------+
                            |
                 +----------+-----------+
                 |                      |
                 v                      v
       +------------------+   +---------------------+
       | Duplicate        |   | Qdrant Vector Index |
       | Detection       |   | Semantic Retrieval  |
       +------------------+   +---------------------+
```

The diagram represents the target workflow. OCR and LLM extraction are
not presented as fully production-ready integrations.

## Project Structure

The repository is organized by responsibility. The structure below
reflects the main components used or planned in the current
implementation.

``` text
ai-invoice-intelligence/
├── app/
│   ├── db/
│   │   ├── base.py
│   │   └── database.py
│   ├── models/
│   │   └── invoice.py
│   ├── repositories/
│   │   └── invoice_repository.py
│   ├── schemas/
│   │   ├── invoice.py
│   │   └── validation.py
│   ├── services/
│   │   ├── pdf_processor.py
│   │   ├── image_processor.py
│   │   ├── document_processor.py
│   │   ├── financial_validator.py
│   │   ├── duplicate_detector.py
│   │   ├── qdrant_store.py
│   │   └── invoice_rag.py
│   └── main.py
├── database/
│   ├── invoices.db              # Generated locally; not committed
│   └── qdrant_storage/          # Generated locally; not committed
├── sample_data/
├── tests/
├── init_db.py
├── run_document.py
├── test_duplicate_detection.py
├── test_rag.py
├── .env.example
├── .gitignore
└── README.md
```

Some files and directories may be added or adjusted as development
progresses.

## Getting Started

### Prerequisites

-   Python 3.11 or a compatible Python version for the installed
    dependencies.
-   Git.
-   Windows, Linux, or macOS.
-   Internet access for installing packages and downloading the
    embedding model on its first use.

> **Windows note:** If you use a Python version that is not supported by
> one of the optional OCR dependencies, use a separate compatible
> virtual environment for that component.

### 1. Clone the repository

``` bash
git clone https://github.com/mosyiran/ai-invoice-intelligence.git
cd ai-invoice-intelligence
```

Replace the repository URL above if the GitHub repository has a
different owner or name.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Git Bash:**

``` bash
python -m venv .venv
source .venv/Scripts/activate
```

**Linux / macOS:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn pydantic sqlalchemy python-dotenv pymupdf pillow opencv-python numpy "qdrant-client[fastembed]"
```

If a `requirements.txt` file is added to the repository, dependency
installation can instead use:

``` bash
python -m pip install -r requirements.txt
```

### 4. Initialize the SQLite database

From the project root:

``` bash
python init_db.py
```

This creates the local SQLite database and the `invoices` table if they
do not already exist.

### 5. Run the API foundation

``` bash
uvicorn app.main:app --reload
```

Open the following local addresses:

-   API root: `http://127.0.0.1:8000/`
-   Health check: `http://127.0.0.1:8000/health`
-   Interactive API documentation: `http://127.0.0.1:8000/docs`

The API currently provides the application foundation; the complete
invoice workflow is being integrated incrementally.

## Running Tests and Scripts

Run commands from the repository root with the virtual environment
activated.

### Duplicate detection

``` bash
python test_duplicate_detection.py
```

The duplicate detection examples cover exact duplicates, normalized
identifiers, and potential duplicates.

### Qdrant indexing and semantic search

``` bash
python test_rag.py
```

The RAG test script indexes invoice records available in SQLite and runs
a sample semantic query.

On the first run, FastEmbed may need to download the embedding model.
The current example uses `sentence-transformers/all-MiniLM-L6-v2`, which
is primarily intended for English text.

## Data and Storage

-   **SQLite** stores structured invoice records and is the source of
    truth.
-   **Qdrant** stores vector representations and payloads used for
    semantic retrieval.
-   The local database and vector-storage directories are generated at
    runtime and should not be committed to Git.

For production deployments with concurrent application workers or
multiple application instances, review the storage architecture. A
server-based database such as PostgreSQL and a separately managed Qdrant
service may be more appropriate than local embedded storage.

## Current Limitations

-   OCR integration and model compatibility need further validation.
-   LLM-based extraction is still an integration task and depends on the
    selected provider, model availability, API access, and
    configuration.
-   The current embedding model is English-oriented; multilingual or
    Persian invoices require an appropriate multilingual embedding model
    and evaluation.
-   Potential duplicate detection is a warning mechanism, not proof that
    two invoices are identical.
-   The local Qdrant storage configuration is intended for development
    and single-process use.
-   Authentication, authorization, production observability, migrations,
    and deployment hardening are not yet complete.

## Roadmap

-   [x] Initial project structure and FastAPI foundation
-   [x] PDF and image processing foundation
-   [x] Pydantic invoice schema
-   [x] Financial validation foundation
-   [x] SQLite database and SQLAlchemy model
-   [x] Invoice repository and CRUD foundations
-   [x] Exact, normalized, and potential duplicate detection
-   [ ] Complete and validate OCR integration
-   [ ] Finalize provider-independent LLM extraction
-   [ ] Complete and evaluate Qdrant-based RAG
-   [ ] Build multi-agent workflow with LangGraph
-   [ ] Integrate invoice workflows into FastAPI
-   [ ] Build a Streamlit dashboard
-   [ ] Add comprehensive automated tests
-   [ ] Add Docker and CI/CD
-   [ ] Production hardening, monitoring, and documentation

The checklist describes the development plan and may change as
implementation and testing progress.

## Security

-   Never commit `.env` files, API keys, credentials, or private invoice
    documents.
-   Keep local database files and Qdrant storage out of version control.
-   Use `.env.example` only for placeholder variable names, never real
    secrets.
-   Treat invoice contents as sensitive financial data and apply
    appropriate access controls before using real customer documents.

## Contributing

This project is under active development. Suggestions, bug reports, and
pull requests are welcome. For substantial changes, open an issue first
to discuss the proposed implementation.

## License

No license has been specified yet. Until a license is added to the
repository, reuse, redistribution, and modification permissions should
not be assumed.

## Author

**Mohsen Goudarzi**

-   GitHub: [@mosyiran](https://github.com/mosyiran)
