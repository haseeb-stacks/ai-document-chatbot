# Deployment Guide (Vertex AI & Cloud Run)

This project is optimized for deployment on Google Cloud Platform using **Vertex AI** and **Cloud Run**. This serverless architecture provides high performance, automatic scaling, and minimal maintenance.

## 🚀 Automated Deployment

The easiest way to deploy is using the provided `deploy_gcp.sh` script.

1.  **Grant Permissions**:
    ```bash
    chmod +x deploy_gcp.sh
    ```

2.  **Run Deploy**:
    ```bash
    ./deploy_gcp.sh
    ```

## 🛠️ Manual Deployment Steps

If you prefer to run commands manually, follow these steps:

### 1. Project Configuration
Replace `YOUR_PROJECT_ID` with your actual GCP project ID.
```bash
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs
```bash
gcloud services enable \
    aiplatform.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com
```

### 3. Grant IAM Roles for Vertex AI
The Cloud Run service account needs permission to call the Gemini API.
```bash
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)')
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/aiplatform.user"
```

### 4. Build and Push to Artifact Registry
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/YOUR_PROJECT_ID/chatbot-repo/ai-doc-chatbot:latest
```

### 5. Deploy to Cloud Run
```bash
gcloud run deploy ai-doc-chatbot \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/chatbot-repo/ai-doc-chatbot:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
```

## 💻 Local Development with Vertex AI

To run the application locally while still using the cloud-based Vertex AI models:

1.  **Login to Application Default Credentials**:
    ```bash
    gcloud auth application-default login
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Run with Project ID**:
    ```bash
    export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
    python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
    ```

## 🔍 Troubleshooting

-   **404 Model Not Found**: Ensure you are using a supported model version (e.g., `gemini-2.0-flash`). Check the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden).
-   **Permission Denied**: Double-check that the `roles/aiplatform.user` role is granted to the correct service account.
-   **Initialization Wait**: On its first start, the app will index the PDFs in the `/data` folder. Subsequent chats will be near-instant.
