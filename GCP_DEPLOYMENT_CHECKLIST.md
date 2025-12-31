# GCP Deployment Checklist

## Code Changes ✅ (Already Done)
- [x] Updated `settings.py` for GCP configuration
- [x] Updated `Dockerfile` for Cloud Run (gunicorn + migrations)
- [x] Updated `requirements.txt` with GCP dependencies
- [x] Updated `storage_backend.py` for Google Cloud Storage
- [x] Created `app.yaml` for App Engine (if needed)
- [x] Created `.env.example` with GCP variables

## Before Deployment
- [ ] Copy `.env.example` to `.env` and fill in real values
- [ ] Generate a new `SECRET_KEY` for production
- [ ] Generate a new `COOKIE_SECRET` for production
- [ ] Prepare database password
- [ ] Prepare email credentials

## GCP Infrastructure Setup
- [ ] Create GCP Project (or use `anwesha-26-472317`)
- [ ] Enable required APIs:
  - [ ] Cloud Run API
  - [ ] Cloud SQL Admin API
  - [ ] Container Registry API
  - [ ] Secret Manager API
  - [ ] Cloud Storage API
- [ ] Create Cloud SQL MySQL instance (8.0)
- [ ] Create database `anwesha_db`
- [ ] Create database user `anwesha_user`
- [ ] Create service account `anwesha-service`
- [ ] Grant Cloud SQL Client role to service account
- [ ] Create Cloud Storage bucket `anwesha-storage-bucket`
- [ ] Grant storage permissions to service account

## Docker & Deployment
- [ ] Authenticate Docker: `gcloud auth configure-docker`
- [ ] Build Docker image
- [ ] Push to Google Container Registry
- [ ] Deploy to Cloud Run with environment variables
- [ ] Set up secret environment variables in Secret Manager
- [ ] Update ALLOWED_HOSTS with Cloud Run domain
- [ ] Update CSRF_TRUSTED_ORIGINS with Cloud Run domain
- [ ] Update CORS_ALLOWED_ORIGINS with Cloud Run domain

## Post-Deployment
- [ ] Run migrations on Cloud SQL
- [ ] Collect static files to Cloud Storage
- [ ] Test API endpoints
- [ ] Test payment flow (update ATOM_RETURN_URL)
- [ ] Test file uploads (profile pictures, QR codes)
- [ ] Check Cloud Run logs for errors
- [ ] Set up monitoring & alerts

## Configuration Values to Update Later
```
CLOUD_SQL_CONNECTION_NAME=anwesha-26-472317:asia-south1:anwesha-mysql  (update region/instance if different)
DB_NAME=anwesha_db
DB_USER=anwesha_user
DB_PASSWORD=<your-secure-password>
GCP_PROJECT_ID=anwesha-26-472317
GCS_BUCKET_NAME=anwesha-storage-bucket
ALLOWED_HOSTS=<your-cloud-run-domain>.run.app
CSRF_TRUSTED_ORIGINS=https://<your-cloud-run-domain>.run.app
CORS_ALLOWED_ORIGINS=https://<your-cloud-run-domain>.run.app
ATOM_RETURN_URL=https://<your-cloud-run-domain>.run.app/response/
```

## Files Modified/Created
- ✅ `anwesha/settings.py` - GCP configuration added
- ✅ `Dockerfile` - Updated for Cloud Run
- ✅ `requirements.txt` - Added GCP dependencies
- ✅ `anwesha/storage_backend.py` - Added GCS support
- ✅ `app.yaml` - Created for App Engine (optional)
- ✅ `.env.example` - Created with all required variables
- ✅ `GCP_DEPLOYMENT.md` - Detailed deployment guide

## Quick Commands

```bash
# Test locally with GCP settings
CONFIGURATION=gcp DEBUG=False python manage.py runserver

# Build and push Docker image
docker build -t gcr.io/anwesha-26-472317/anwesha-backend:latest .
docker push gcr.io/anwesha-26-472317/anwesha-backend:latest

# Deploy to Cloud Run
gcloud run deploy anwesha-backend \
  --image=gcr.io/anwesha-26-472317/anwesha-backend:latest \
  --region=asia-south1 \
  --add-cloudsql-instances=anwesha-26-472317:asia-south1:anwesha-mysql \
  --service-account=anwesha-service@anwesha-26-472317.iam.gserviceaccount.com

# View logs
gcloud run logs read anwesha-backend --region=asia-south1
```
