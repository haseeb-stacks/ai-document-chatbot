# Deployment Instructions

This project uses FastAPI, LangChain, and Ollama. It can be run locally or deployed to Google Cloud Platform (GCP).

## Local Development

1.  **Dependencies**: Ensure you are in the `agent` conda environment.
    ```bash
    conda activate agent
    pip install -r backend/requirements.txt
    ```

2.  **Ollama**: Ensure Ollama is installed and running.
    ```bash
    ollama serve
    ollama pull gemma3:4b
    ```

3.  **Run**:
    ```bash
    python backend/app/main.py
    ```
    Access the UI at `http://localhost:8000`.

## Docker & GCP Deployment

Since this application requires a running LLM (Ollama), it needs sufficient memory (4GB+ recommended) and the container image will be larger than typical web apps.

### 1. Build Docker Image

```bash
docker build -t ai-doc-chatbot .
```

### 2. Test Docker Locally

```bash
docker run -p 8000:8000 -e OLLAMA_MODEL=gemma2:2b ai-doc-chatbot
```
*Note: We use `gemma2:2b` in Docker to keep the download size manageable. You can change this in `entrypoint.sh` or via the env var.*

### 3. Deploy to Google Cloud Run

**Prerequisites**:
- Google Cloud SDK (`gcloud`) installed and authenticated.
- A GCP Project with billing enabled.

**Steps**:

1.  **Configure Project**:
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```

2.  **Enable Artifact Registry**:
    ```bash
    gcloud services enable artifactregistry.googleapis.com run.googleapis.com
    ```

3.  **Build & Submit Image**:
    ```bash
    gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-doc-chatbot
    ```

4.  **Deploy to Cloud Run**:
    ```bash
    gcloud run deploy ai-doc-chatbot \
      --image gcr.io/YOUR_PROJECT_ID/ai-doc-chatbot \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --memory 4Gi \
      --cpu 2 \
      --timeout 300
    ```
    *Important: We increase memory to 4Gi and CPU to 2 to handle the LLM.*

### Troubleshooting

-   **Ollama Connection**: The app waits for Ollama to be ready. If deployment times out, increase the `--timeout` or check logs.
-   **Cold Starts**: The first request might differ as the model loads into memory.
