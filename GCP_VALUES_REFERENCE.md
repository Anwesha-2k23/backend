# GCP Deployment Values Reference

## Project Information
- **GCP Project ID**: `anwesha-26-472317`
- **Region**: `asia-south1` (India)
- **Service Account**: `anwesha-service@anwesha-26-472317.iam.gserviceaccount.com`

## Cloud SQL
- **Instance Name**: `anwesha-mysql`
- **Region**: `asia-south1`
- **Engine**: MySQL 8.0
- **Connection Name Format**: `anwesha-26-472317:asia-south1:anwesha-mysql`
- **Database Name**: `anwesha_db`
- **Database User**: `anwesha_user`
- **Database Password**: `[TO BE CREATED]`
- **Instance Type**: `db-f1-micro` (or upgrade as needed)

## Cloud Storage
- **Bucket Name**: `anwesha-storage-bucket`
- **Region**: `asia-south1`
- **Bucket URL**: `gs://anwesha-storage-bucket`
- **Public URL Pattern**: `https://storage.googleapis.com/anwesha-storage-bucket/...`

## Cloud Run
- **Service Name**: `anwesha-backend`
- **Region**: `asia-south1`
- **Memory**: `512Mi` (can be increased if needed)
- **CPU**: `1` (can be increased if needed)
- **Instances**: Min 1, Max 10 (auto-scaling)
- **Port**: `8080` (internally)
- **Public URL**: `https://anwesha-backend-XXXXX.run.app` (assigned after deployment)

## Environment Variables to Set
```env
# Django Settings
CONFIGURATION=gcp
DEBUG=False
SECRET_KEY=[GENERATE NEW - min 50 chars]

# Database
CLOUD_SQL_CONNECTION_NAME=anwesha-26-472317:asia-south1:anwesha-mysql
DB_NAME=anwesha_db
DB_USER=anwesha_user
DB_PASSWORD=[CREATE IN GCP]

# GCP
GCP_PROJECT_ID=anwesha-26-472317
GCP_STORAGE_ENABLED=True
GCS_BUCKET_NAME=anwesha-storage-bucket

# Security
COOKIE_SECRET=[GENERATE NEW]

# CORS & CSRF
ALLOWED_HOSTS=anwesha-backend-XXXXX.run.app,yourdomain.com
CSRF_TRUSTED_ORIGINS=https://anwesha-backend-XXXXX.run.app,https://yourdomain.com
CORS_ALLOWED_ORIGINS=https://anwesha-backend-XXXXX.run.app,https://yourdomain.com

# Email
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=[APP-SPECIFIC PASSWORD]

# Payment (Atom Pay)
ATOM_MERCHANT_ID=564719
ATOM_MERCHANT_PASSWORD=anwesha@24
ATOM_RETURN_URL=https://anwesha-backend-XXXXX.run.app/response/
```

## Docker Image
- **Image Name**: `gcr.io/anwesha-26-472317/anwesha-backend`
- **Latest Tag**: `:latest`
- **Registry**: Google Container Registry (GCR)
- **Registry URL**: `gcr.io`

## API Endpoints (Post-Deployment)
Replace `CLOUD_RUN_URL` with your Cloud Run domain:

```
Base URL: https://CLOUD_RUN_URL

Auth:
- POST /user/login/ - User login
- POST /user/logout/ - User logout
- GET  /user/get_user_data/ - Get user info

Events:
- GET  /event/events/ - List events
- POST /event/register/ - Register for event
- GET  /event/my_events/ - Get user's events

Payment:
- POST /atompay/ - Get Atom token
- POST /response/ - Payment callback

Admin:
- /admin/ - Django admin panel
```

## Security Notes
- **Never commit** `.env` file to repository
- **Generate new** `SECRET_KEY` and `COOKIE_SECRET` for production
- **Use Google Secret Manager** for sensitive values (passwords, API keys)
- **Enable SSL/TLS** (Cloud Run does this automatically)
- **Use HTTPS only** in production
- **Set proper CORS** origins to avoid unauthorized requests

## Cost Estimation
- **Cloud SQL (db-f1-micro)**: ~$9/month
- **Cloud Run (with auto-scaling)**: ~$0.00002400 per vCPU-second + ~$0.40 per GB-month
- **Cloud Storage**: ~$0.020 per GB for first 1TB
- **Total estimated**: $15-30/month for low traffic

## Monitoring & Logs
- **Cloud Run Logs**: `gcloud run logs read anwesha-backend --region=asia-south1`
- **Cloud SQL Logs**: GCP Console > Cloud SQL > Logs
- **Error Tracking**: GCP Console > Error Reporting
- **Application Metrics**: GCP Console > Cloud Run > Metrics

## Backup Strategy
```bash
# Export database
gcloud sql export sql anwesha-mysql \
  gs://anwesha-storage-bucket/backups/anwesha-$(date +%Y%m%d).sql \
  --database=anwesha_db

# Restore database
gcloud sql import sql anwesha-mysql \
  gs://anwesha-storage-bucket/backups/anwesha-20231223.sql \
  --database=anwesha_db
```

## Useful Links
- GCP Console: https://console.cloud.google.com/
- Cloud Run Dashboard: https://console.cloud.google.com/run
- Cloud SQL Console: https://console.cloud.google.com/sql
- GCP Documentation: https://cloud.google.com/docs
- Django Deployment Guide: https://docs.djangoproject.com/en/4.1/howto/deployment/
