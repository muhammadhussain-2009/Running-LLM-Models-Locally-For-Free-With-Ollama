# Multi PDFS Chatbot RAG Project — Chat with PDFs (Google Generative AI + FAISS)

A small Retrieval-Augmented Generation (RAG) demo that lets you upload one or more PDF documents, builds an embeddings-based vector index (FAISS) and answers user questions using Google Generative AI (chat + embedding models) via a Streamlit UI.

This README explains what the project does, how it works, how to install and run it locally, configuration, troubleshooting tips, and recommended improvements.

---

Table of contents
- [Project overview](#project-overview)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment configuration (.env)](#environment-configuration-env)
- [Running the app](#running-the-app)
- [How it works (pipeline)](#how-it-works-pipeline)
- [Files and structure](#files-and-structure)
- [Index persistence and storage](#index-persistence-and-storage)
- [Troubleshooting & common issues](#troubleshooting--common-issues)
- [Customization & suggestions](#customization--suggestions)
- [Security and privacy notes](#security-and-privacy-notes)
- [Contributing](#contributing)
- [License](#license)

---

## Project overview

This project provides a simple Streamlit web app that:

1. Accepts PDF uploads from the user.
2. Extracts text from uploaded PDFs.
3. Splits the text into chunks (for context windows).
4. Creates embeddings for chunks using Google Generative AI Embeddings.
5. Stores embeddings in a FAISS vector index (locally).
6. At query time, performs similarity search and uses a Google chat model to answer questions using retrieved context.

It is intended as a minimal example / starter for building locally-hosted RAG applications that use Google Generative AI (GenAI) models for embeddings and chat.

---

## Features

- Upload multiple PDFs from the browser.
- Text extraction from PDFs (PyPDF2).
- Text chunking with overlap to preserve context.
- Embeddings using Google Generative AI Embeddings.
- Vector search using FAISS (local).
- Question answering via Google chat model (ChatGoogleGenerativeAI) using a "stuff" QA chain.
- Simple Streamlit UI.

---

## Tech stack

- Python >= 3.11
- Streamlit (web UI)
- PyPDF2 (PDF parsing)
- Google Generative AI SDK (google-generativeai)
- langchain and langchain-community integrations
- FAISS (faiss-cpu)
- python-dotenv (manage .env with API keys)

See `pyproject.toml` and `requirements.txt` for pinned dependencies included in the project.

---

## Prerequisites

- Python 3.11+ (the project metadata states >=3.11)
- A Google Generative AI API key (set in `GOOGLE_API_KEY`)
- A working C/C++ build toolchain or use `faiss-cpu` wheels (platform-dependent). On some platforms it’s easier to install via conda-forge:
  - conda: `conda install -c conda-forge faiss-cpu`
  - or use pip: `pip install faiss-cpu`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/muhammadhussain-2009/Locally-Hosted-LLM-Projects.git
   cd "Locally-Hosted-LLM-Projects/RAG Project"
   ```

   Note: The folder name contains a space (`RAG Project`). You can use quotes or escape the space when changing directories.

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   - If you prefer pip / requirements.txt:
     ```bash
     pip install -r requirements.txt
     ```
   - Or install from `pyproject.toml` (PEP 517 install or editable install):
     ```bash
     pip install -e .
     ```
   If faiss fails to install via pip on your platform, prefer conda:
   ```bash
   conda install -c conda-forge faiss-cpu
   ```

---

## Environment configuration (.env)

Create a `.env` file in the same directory as `ChatBot.py` with the following:

```env
# .env
GOOGLE_API_KEY=your_google_genai_api_key_here
```

Important:
- Never commit your `.env` or API keys to version control. This repo's `.gitignore` already ignores common Python artifacts and a `.venv` entry; add `.env` if not already ignored.

---

## Running the app

Run the Streamlit app from the project directory (note the space in the path):

```bash
# from project root where ChatBot.py is located
streamlit run "ChatBot.py"
```

Or, if executing from the parent folder:

```bash
streamlit run "RAG Project/ChatBot.py"
```

Workflow in the UI:
1. Click the file uploader and add one or more PDF files.
2. Click the "Process" button to:
   - Extract text from PDFs
   - Split text into chunks
   - Generate embeddings and build a FAISS index (saved to `faiss_index/`)
3. Enter a question in the "Ask a question about your PDFs:" text box.
4. Click "Get Answer" to run similarity search + QA chain and display the answer.

---

## How it works (pipeline)

1. PDF ingestion
   - The UI accepts uploaded PDF files.
   - Text is extracted page-by-page using PyPDF2 PdfReader.

2. Chunking
   - Text is split using a recursive character splitter (chunk_size 1000, overlap 200 by default) to create manageable pieces of context for the embedding model.

3. Embeddings
   - Chunks are embedded using GoogleGenerativeAIEmbeddings (model: `"models/embedding-001"` in code).
   - Each chunk produces a vector embedding.

4. Vector store (FAISS)
   - Embeddings + original text chunks are inserted into a FAISS index using the langchain-community FAISS wrapper.
   - The index is saved locally under `faiss_index/`.

5. Query / QA
   - On user query, the app runs a similarity search on the FAISS index to retrieve the most relevant chunks.
   - The retrieved chunks are passed to a ChatGoogleGenerativeAI model (`"models/chat-bison-001"`) via a QA chain.
   - The LLM generates a concise response using the provided context (the code uses a "stuff" chain type).

---

## Files and structure

- ChatBot.py
  - Main Streamlit application.
  - Implements: PDF upload → text extraction → chunking → embedding → FAISS index creation/loading → QA chain + query UI.

- pyproject.toml / requirements.txt
  - Dependency lists and project metadata.

- .gitignore
  - Ignores Python cache, virtual environment folder, build artifacts.

- Generated at runtime:
  - `faiss_index/` — directory where the FAISS index and related metadata are stored.

---

## Index persistence and storage

- The FAISS index is stored locally in the `faiss_index` directory (created by `FAISS.from_texts(...).save_local("faiss_index")`).
- To rebuild the index:
  - Re-run the "Process" step in the UI after (re)uploading PDFs.
  - Or delete `faiss_index/` and re-run processing.

---

## Troubleshooting & common issues

- Missing GOOGLE_API_KEY or invalid key
  - Symptom: the app cannot call Google Generative AI APIs and returns authorization errors.
  - Fix: Ensure `.env` exists with `GOOGLE_API_KEY` and that `load_dotenv()` reads it. Restart the Streamlit app after editing `.env`.

- PyPDF2 extraction returns None or empty text
  - Some PDFs (scanned images) have no extractable text; OCR is required (Tesseract or other OCR tools).
  - Fix: Pre-OCR PDFs or use a PDF parsing pipeline that integrates OCR.

- FAISS installation issues
  - FAISS can be tricky to install on some platforms. If `pip install faiss-cpu` fails, try:
    - conda: `conda install -c conda-forge faiss-cpu`
    - Use the platform-appropriate wheel if available.

- Model names / API compatibility
  - Model names used in code: `"models/embedding-001"` and `"models/chat-bison-001"`. These are based on the current codebase and may change with Google SDK updates. If you see "model not found" errors, check the `google-generativeai` SDK docs for the correct model names and update accordingly.

- Streamlit path with spaces
  - If your path contains spaces (`RAG Project`), wrap the path in quotes when running Streamlit: `streamlit run "RAG Project/ChatBot.py"`

- Import errors (langchain package surface)
  - If you see import errors like `ModuleNotFoundError` for `langchain_text_splitters` or `langchain_google_genai`, ensure you have the matching `langchain`, `langchain-community`, and `langchain-google-genai` package versions installed. If necessary, consult the upstream packages' docs for the correct import paths — package API may evolve between versions.

- Zero or irrelevant results from similarity search
  - Ensure the FAISS index is built after uploading and processing PDFs.
  - Check that chunking settings are appropriate for your documents: too-large chunks may lose focus; too-small chunks may remove context.

---

## Customization & suggestions

- Change chunk size / overlap
  - Edit `get_chunks()` in `ChatBot.py` to tune `chunk_size` and `chunk_overlap` for your documents.

- Use a different embedding or chat model
  - Replace model names or embeddings class in `get_vector_store`, `load_vector_store`, and `get_conversation_chain`.

- Add OCR for scanned PDFs
  - Integrate Tesseract (pytesseract) or an OCR cloud service to extract text from images.

- Use a different vector store (Milvus, Pinecone, Weaviate)
  - Swap out FAISS with another vector backend for scalability and remote indexing.

- Add caching and persistence improvements
  - Track which files were used to build the index and rebuild only when documents change.

- Improve prompt and chain type
  - The project uses a "stuff" chain; for larger contexts, consider `map_reduce` or `refine` chain types or an explicit retrieval-augmented prompt template.

---

## Security and privacy notes

- The app sends document content to Google Generative AI for embeddings and chat. Do not upload sensitive or private documents unless you're comfortable with the privacy/terms of the model/service.
- Keep API keys secret. Add `.env` to `.gitignore` if not already ignored.
- If you plan to deploy publicly, add authentication and rate-limiting.

---

## Contributing

Contributions, issues, and feature requests are welcome:

- If you find a bug, please open an issue in the upstream repository.
- PRs should follow the code style and include a short description of changes.

Before contributing:
- Ensure you can reproduce the project locally.
- Document changes to README or code where appropriate.

---
