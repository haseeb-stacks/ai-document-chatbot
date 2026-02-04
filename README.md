# AI Document Chatbot

A RAG (Retrieval-Augmented Generation) based chatbot that allows users to interact with PDF documents using a local LLM (Gemma) via Ollama.

## Features

-   **RAG Engine**: Ingests PDFs, chunks text, creates embeddings, and retrieves relevant context.
-   **Local LLM**: Uses Google's Gemma model via Ollama for privacy and offline capability.
-   **Modern UI**: A responsive, dark-mode web interface built with clean HTML/CSS/JS.
-   **FastAPI Backend**: Robust generic API handling ingestion and chat.
-   **Dockerized**: Ready for cloud deployment with self-containment.

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI entry point
│   │   └── rag.py        # RAG logic (LangChain + Ollama)
│   └── requirements.txt  # Python dependencies
├── data/                 # Place PDF documents here
├── frontend/             # Single Page Application
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── Dockerfile            # Container definition
├── entrypoint.sh         # Startup script
└── DEPLOY.md             # Deployment guide
```

## Quick Start (Local)

1.  **Prerequisites**:
    -   Python 3.11+
    -   [Ollama](https://ollama.com/) installed
    -   Run `ollama pull gemma3:4b`

2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Run Application**:
    ```bash
    python backend/app/main.py
    ```

4.  **Access**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.

## Deployment

See [DEPLOY.md](DEPLOY.md) for detailed instructions on deploying to Google Cloud Platform.
