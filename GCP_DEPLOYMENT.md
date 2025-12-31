# GCP Cloud Run Deployment Guide

## Prerequisites
- GCP Account with project `anwesha-26-472317`
- Google Cloud SDK installed (`gcloud` CLI)
- Docker installed locally

## Step 1: Create Cloud SQL MySQL Instance

```bash
# Create Cloud SQL MySQL instance
gcloud sql instances create anwesha-mysql \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=asia-south1 \
  --project=anwesha-26-472317

# Create database
gcloud sql databases create anwesha_db \
  --instance=anwesha-mysql \
  --project=anwesha-26-472317

# Create user
gcloud sql users create anwesha_user \
  --instance=anwesha-mysql \
  --password=YOUR_SECURE_PASSWORD \
  --project=anwesha-26-472317

# Get connection name (you'll need this)
gcloud sql instances describe anwesha-mysql --project=anwesha-26-472317
# Look for: connectionName: anwesha-26-472317:asia-south1:anwesha-mysql
```

## Step 2: Create Cloud Storage Bucket (for static/media files)

```bash
# Create bucket
gsutil mb -l asia-south1 gs://anwesha-storage-bucket

# Make bucket publicly readable for static files
gsutil iam ch serviceAccount:anwesha-service@anwesha-26-472317.iam.gserviceaccount.com:roles/storage.objectViewer gs://anwesha-storage-bucket
```

## Step 3: Set Up Service Account

```bash
# Create service account
gcloud iam service-accounts create anwesha-service \
  --display-name="Anwesha Backend Service" \
  --project=anwesha-26-472317

# Grant Cloud SQL Client permission
gcloud projects add-iam-policy-binding anwesha-26-472317 \
  --member=serviceAccount:anwesha-service@anwesha-26-472317.iam.gserviceaccount.com \
  --role=roles/cloudsql.client

# Grant Cloud Storage permissions
gcloud projects add-iam-policy-binding anwesha-26-472317 \
  --member=serviceAccount:anwesha-service@anwesha-26-472317.iam.gserviceaccount.com \
  --role=roles/storage.objectAdmin
```

## Step 4: Create `.env` File for Production

```bash
cp .env.example .env

# Edit .env with production values:
```

**.env (update these):**
```
DEBUG=False
CONFIGURATION=gcp
SECRET_KEY=generate-a-new-strong-secret-key
CLOUD_SQL_CONNECTION_NAME=anwesha-26-472317:asia-south1:anwesha-mysql
DB_NAME=anwesha_db
DB_USER=anwesha_user
DB_PASSWORD=YOUR_SECURE_PASSWORD
GCP_PROJECT_ID=anwesha-26-472317
GCP_STORAGE_ENABLED=True
GCS_BUCKET_NAME=anwesha-storage-bucket
COOKIE_SECRET=generate-a-new-secret
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ALLOWED_HOSTS=your-cloud-run-domain.run.app,yourdomain.com
CSRF_TRUSTED_ORIGINS=https://your-cloud-run-domain.run.app,https://yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-cloud-run-domain.run.app,https://yourdomain.com
ATOM_RETURN_URL=https://your-cloud-run-domain.run.app/response/
```

## Step 5: Build and Push Docker Image to Google Container Registry

```bash
# Configure Docker
gcloud auth configure-docker

# Build image
docker build -t gcr.io/anwesha-26-472317/anwesha-backend:latest .

# Push to GCR
docker push gcr.io/anwesha-26-472317/anwesha-backend:latest
```

## Step 6: Deploy to Cloud Run

```bash
# Deploy with environment from .env
gcloud run deploy anwesha-backend \
  --image=gcr.io/anwesha-26-472317/anwesha-backend:latest \
  --platform=managed \
  --region=asia-south1 \
  --memory=512Mi \
  --cpu=1 \
  --service-account=anwesha-service@anwesha-26-472317.iam.gserviceaccount.com \
  --add-cloudsql-instances=anwesha-26-472317:asia-south1:anwesha-mysql \
  --set-env-vars=CONFIGURATION=gcp,DEBUG=False,GCP_PROJECT_ID=anwesha-26-472317,GCP_STORAGE_ENABLED=True,GCS_BUCKET_NAME=anwesha-storage-bucket \
  --project=anwesha-26-472317 \
  --allow-unauthenticated
```

## Step 7: Set Secret Environment Variables

For sensitive values, use Google Secret Manager:

```bash
# Create secrets
echo -n "your-secret-key" | gcloud secrets create SECRET_KEY --data-file=-
echo -n "your-password" | gcloud secrets create DB_PASSWORD --data-file=-
echo -n "your-cookie-secret" | gcloud secrets create COOKIE_SECRET --data-file=-
echo -n "your-email-password" | gcloud secrets create EMAIL_HOST_PASSWORD --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding SECRET_KEY \
  --member=serviceAccount:anwesha-service@anwesha-26-472317.iam.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor
```

## Step 8: Run Migrations

After deployment, run migrations:

```bash
gcloud run execute anwesha-backend \
  --command="python manage.py migrate"
```

Or use Cloud SQL Proxy locally:

```bash
# Download cloud_sql_proxy
# https://cloud.google.com/sql/docs/mysql/sql-proxy

# Run proxy in one terminal
./cloud_sql_proxy -instances=anwesha-26-472317:asia-south1:anwesha-mysql=tcp:3306

# In another terminal, run migrations
python manage.py migrate
python manage.py collectstatic --noinput
```

## Step 9: Update Frontend URLs

Update your frontend to point to the Cloud Run service URL:
```
https://anwesha-backend-xxxxx.run.app
```

## Monitoring & Logs

```bash
# View logs
gcloud run logs read anwesha-backend --region=asia-south1 --limit=50

# Check service status
gcloud run services describe anwesha-backend --region=asia-south1
```

## Useful Commands

```bash
# Redeploy with code changes
docker build -t gcr.io/anwesha-26-472317/anwesha-backend:latest .
docker push gcr.io/anwesha-26-472317/anwesha-backend:latest
gcloud run deploy anwesha-backend --image=gcr.io/anwesha-26-472317/anwesha-backend:latest --region=asia-south1

# Scale instances
gcloud run services update anwesha-backend --region=asia-south1 --max-instances=10

# Delete service
gcloud run services delete anwesha-backend --region=asia-south1
```

## Troubleshooting

**Cloud SQL connection issues:**
- Check if Cloud SQL Admin API is enabled
- Verify service account has `cloudsql.client` role
- Check firewall rules if using Cloud SQL Proxy

**Storage issues:**
- Verify bucket exists: `gsutil ls gs://anwesha-storage-bucket`
- Check permissions on service account
- Ensure `GCP_STORAGE_ENABLED=True` in environment

**Static files not loading:**
- Run: `python manage.py collectstatic --noinput`
- Verify `GCS_BUCKET_NAME` matches your bucket
- Check Cloud Storage public access settings
