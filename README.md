# AI Document Assistant (Cloud-Native RAG)

A high-performance RAG (Retrieval-Augmented Generation) chatbot that allows users to interact with PDF documents. This version is optimized for Google Cloud Platform, using Vertex AI for lightning-fast responses and minimal infrastructure overhead.

## 🚀 Live Demo
**URL**: [https://ai-doc-chatbot-224109816462.us-central1.run.app](https://ai-doc-chatbot-224109816462.us-central1.run.app)

## ✨ Features

-   **Cloud-Native RAG**: Integrated with **Google Vertex AI** for industry-leading response times and accuracy.
-   **Advanced LLM**: Powered by **Gemini 2.0 Flash** via Vertex AI.
-   **High-Quality Embeddings**: Uses `text-embedding-004` (Vertex AI) for superior semantic search.
-   **Modern UI**: Sleek, glassmorphism-inspired dark mode interface with micro-animations.
-   **Scalable Architecture**: Deployed on **Google Cloud Run** for serverless scaling.
-   **FastAPI Backend**: Asynchronous API structure for handling multiple concurrent chat sessions.

## 📁 Project Structure

```text
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI routing & static file serving
│   │   └── rag.py        # RAG implementation (Vertex AI + FAISS)
│   └── requirements.txt  # Pinned cloud dependencies
├── data/                 # Source PDF documents
├── frontend/             # Single Page Application (HTML/CSS/JS)
├── Dockerfile            # Optimized slim container definition
├── deploy_gcp.sh         # Automated GCP deployment script
└── README.md             # Project documentation
```

## 🛠️ Technology Stack

-   **LLM**: Google Gemini 2.0 Flash
-   **Vector DB**: FAISS (Facebook AI Similarity Search)
-   **Framework**: LangChain 0.3
-   **Backend**: FastAPI (Python 3.11)
-   **Deployment**: Google Cloud Run & Artifact Registry

## 💻 Local Development

1.  **Authentication**:
    Ensure you have the Google Cloud SDK installed and authenticated:
    ```bash
    gcloud auth application-default login
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Run Application**:
    ```bash
    export GOOGLE_CLOUD_PROJECT="your-project-id"
    python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
    ```

## ☁️ Cloud Deployment

The project is configured for automated deployment via `deploy_gcp.sh`. It handles:
1. Building an optimized Docker image in Cloud Build.
2. Pushing to Artifact Registry.
3. Deploying to Cloud Run with correct IAM permissions for Vertex AI.

```bash
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

---
Built with ❤️ using Google Vertex AI.
