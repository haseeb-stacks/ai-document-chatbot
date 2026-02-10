#!/bin/bash
set -e

# Usage: ./deploy_gcp.sh [PROJECT_ID] [REGION]

PROJECT_ID=$1
REGION=${2:-us-central1}
APP_NAME="ai-doc-chatbot"
IMAGE_NAME="gcr.io/$PROJECT_ID/$APP_NAME"

if [ -z "$PROJECT_ID" ]; then
    echo "Usage: ./deploy_gcp.sh [PROJECT_ID] [REGION]"
    echo "Please provide your GCP Project ID."
    exit 1
fi

echo "Deploying $APP_NAME to GCP Project: $PROJECT_ID in $REGION"

# 1. Enable services
echo "Enabling necessary GCP services..."
gcloud services enable artifactregistry.googleapis.com run.googleapis.com cloudbuild.googleapis.com --project "$PROJECT_ID"

# 2. Build and push image
echo "Building Docker image (this may take a while to upload contexts)..."
gcloud builds submit --tag "$IMAGE_NAME" --project "$PROJECT_ID"

# 3. Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy "$APP_NAME" \
  --image "$IMAGE_NAME" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300 \
  --project "$PROJECT_ID" \
  --set-env-vars OLLAMA_MODEL=gemma2:2b

echo "Deployment complete!"
echo "Service URL:"
gcloud run services describe "$APP_NAME" --platform managed --region "$REGION" --project "$PROJECT_ID" --format 'value(status.url)'
