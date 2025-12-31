#!/bin/bash

# GCP Cloud Run Deployment Script for Anwesha Backend
# This script automates the deployment process

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ID="anwesha-26-472317"
REGION="asia-south1"
IMAGE_NAME="anwesha-backend"
SERVICE_NAME="anwesha-backend"
REGISTRY="gcr.io"

echo -e "${GREEN}=== Anwesha Backend GCP Deployment ===${NC}\n"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

# Set GCP project
echo -e "${YELLOW}Setting GCP project to: $PROJECT_ID${NC}"
gcloud config set project $PROJECT_ID

# Configure Docker authentication
echo -e "${YELLOW}Configuring Docker authentication...${NC}"
gcloud auth configure-docker

# Build Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t $REGISTRY/$PROJECT_ID/$IMAGE_NAME:latest .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker image built successfully${NC}\n"
else
    echo -e "${RED}✗ Docker build failed${NC}"
    exit 1
fi

# Push to GCR
echo -e "${YELLOW}Pushing image to Google Container Registry...${NC}"
docker push $REGISTRY/$PROJECT_ID/$IMAGE_NAME:latest

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Image pushed successfully${NC}\n"
else
    echo -e "${RED}✗ Image push failed${NC}"
    exit 1
fi

# Deploy to Cloud Run
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
  --image=$REGISTRY/$PROJECT_ID/$IMAGE_NAME:latest \
  --platform=managed \
  --region=$REGION \
  --memory=512Mi \
  --cpu=1 \
  --service-account=anwesha-service@$PROJECT_ID.iam.gserviceaccount.com \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:anwesha-mysql \
  --set-env-vars=CONFIGURATION=gcp,DEBUG=False,GCP_PROJECT_ID=$PROJECT_ID,GCP_STORAGE_ENABLED=True,GCS_BUCKET_NAME=anwesha-storage-bucket \
  --allow-unauthenticated \
  --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Deployment successful${NC}\n"
    
    # Get service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')
    echo -e "${GREEN}Service URL: $SERVICE_URL${NC}\n"
    
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Update .env with your production values"
    echo "2. Run migrations: gcloud run execute $SERVICE_NAME --command='python manage.py migrate'"
    echo "3. Collect static files: gcloud run execute $SERVICE_NAME --command='python manage.py collectstatic --noinput'"
    echo "4. View logs: gcloud run logs read $SERVICE_NAME --region=$REGION"
else
    echo -e "${RED}✗ Deployment failed${NC}"
    exit 1
fi
