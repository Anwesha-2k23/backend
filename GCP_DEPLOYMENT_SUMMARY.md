# GCP Deployment Summary - All Changes Made

## Overview
Your Django backend is now ready for deployment to **Google Cloud Platform** using **Cloud Run** (serverless) + **Cloud SQL MySQL** (managed database) + **Cloud Storage** (static/media files).

## Files Created/Modified

### 1. **anwesha/settings.py** ✅
**Changes Made:**
- Added support for `CONFIGURATION=gcp` mode
- Cloud SQL connection via Unix socket: `/cloudsql/{CLOUD_SQL_CONNECTION_NAME}`
- Environment variables for ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, CORS_ALLOWED_ORIGINS (all configurable)
- Added `GCP_STORAGE_ENABLED` flag to switch between GCS, S3, and local storage
- DEBUG and other settings now read from environment variables

**Key Addition:**
```python
elif CONFIGURATION == 'gcp':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': f"/cloudsql/{env('CLOUD_SQL_CONNECTION_NAME')}",
            ...
        }
    }
```

### 2. **Dockerfile** ✅
**Changes Made:**
- Changed CMD to use Gunicorn instead of `runserver`
- Exposed port `8080` (standard for Cloud Run)
- Added automatic migrations on container startup
- Optimized for production deployment

**Key Change:**
```dockerfile
CMD ["sh", "-c", "python manage.py migrate && gunicorn anwesha.wsgi:application --bind 0.0.0.0:8080 --workers 4"]
```

### 3. **requirements.txt** ✅
**Dependencies Added:**
- `google-cloud-storage==2.10.0` - For Cloud Storage integration
- `gunicorn==21.2.0` - Production WSGI server
- `Pillow==9.5.0` - Image processing
- `pycryptodome==3.18.0` - Cryptography (already needed)
- `setuptools==67.8.0` - Build tools

### 4. **anwesha/storage_backend.py** ✅
**Changes Made:**
- Added Google Cloud Storage backend support
- Conditional loading based on `GCP_STORAGE_ENABLED`
- Storage classes work with GCS for profile images, QR codes, gallery, etc.

**Priority Order:**
1. If `GCP_STORAGE_ENABLED=True` → Use Google Cloud Storage
2. Else if `S3_ENABLED=True` → Use AWS S3
3. Else → Use local filesystem

### 5. **app.yaml** ✅ (NEW)
**Purpose:** Google App Engine deployment configuration (alternative to Cloud Run)
- Auto-scaling configuration
- Health check settings
- Cloud SQL binding
- Environment variables

### 6. **.env.example** ✅ (NEW)
**Purpose:** Template for all required environment variables
**Includes:**
- Django settings
- Database configuration
- GCP configuration
- Email setup
- Payment (Atom Pay) settings
- CORS/CSRF settings

**Note:** Copy this and fill in real values for production

### 7. **GCP_DEPLOYMENT.md** ✅ (NEW)
**Purpose:** Step-by-step deployment guide
**Covers:**
- Cloud SQL setup
- Cloud Storage bucket creation
- Service account configuration
- Docker build & push
- Cloud Run deployment
- Migrations & static files collection
- Monitoring & troubleshooting

### 8. **GCP_DEPLOYMENT_CHECKLIST.md** ✅ (NEW)
**Purpose:** Quick reference checklist before, during, and after deployment

### 9. **GCP_VALUES_REFERENCE.md** ✅ (NEW)
**Purpose:** Keep track of all GCP-specific values and endpoints
**Includes:**
- Project ID, regions, resource names
- Backup strategies
- Cost estimation
- Useful commands

### 10. **deploy-to-gcp.sh** ✅ (NEW)
**Purpose:** Automated deployment bash script
**Does:**
- Authenticates with GCP
- Builds Docker image
- Pushes to Google Container Registry
- Deploys to Cloud Run
- Provides service URL

## Key Configuration Values

**Hardcoded:**
```
PROJECT_ID: anwesha-26-472317
REGION: asia-south1 (India)
SERVICE_ACCOUNT: anwesha-service@anwesha-26-472317.iam.gserviceaccount.com
```

**To be Created/Configured:**
```
CONFIGURATION=gcp
DEBUG=False
SECRET_KEY=[NEW - generate 50+ chars]
COOKIE_SECRET=[NEW - generate]
CLOUD_SQL_CONNECTION_NAME=anwesha-26-472317:asia-south1:anwesha-mysql
DB_PASSWORD=[Create in GCP]
GCP_STORAGE_ENABLED=True
ALLOWED_HOSTS=[Your Cloud Run domain]
CSRF_TRUSTED_ORIGINS=[Your Cloud Run domain]
EMAIL_HOST_PASSWORD=[Your email app password]
ATOM_RETURN_URL=[Your Cloud Run domain]/response/
```

## Workflow (What You Do Next)

### Phase 1: GCP Setup (Infrastructure)
1. Create Cloud SQL MySQL instance with connection name: `anwesha-26-472317:asia-south1:anwesha-mysql`
2. Create database: `anwesha_db`
3. Create user: `anwesha_user`
4. Create Cloud Storage bucket: `anwesha-storage-bucket`
5. Create service account: `anwesha-service@anwesha-26-472317.iam.gserviceaccount.com`
6. Grant Cloud SQL & Storage permissions to service account

### Phase 2: Prepare Code
1. Copy `.env.example` to `.env`
2. Fill in all required values (see GCP_VALUES_REFERENCE.md)
3. Run locally to test: `CONFIGURATION=gcp DEBUG=False python manage.py runserver`

### Phase 3: Build & Deploy
1. Run: `bash deploy-to-gcp.sh` (automated)
   - OR manually follow steps in GCP_DEPLOYMENT.md
2. Docker image builds, pushes to GCR, deploys to Cloud Run
3. Get service URL from output

### Phase 4: Post-Deployment
1. Run migrations: `python manage.py migrate` (via Cloud SQL Proxy)
2. Collect static files to Cloud Storage
3. Test API endpoints
4. Update frontend to use new Cloud Run URL
5. Test payment flow with new `ATOM_RETURN_URL`

## Important Notes

⚠️ **Do NOT commit `.env` file to Git** - Only commit `.env.example`

⚠️ **Database Connection** - Cloud Run uses Unix socket to connect to Cloud SQL automatically (no network connection needed)

⚠️ **Static Files** - Will be served from Cloud Storage, not from disk. Make sure to run `collectstatic` after deployment

⚠️ **Migrations** - Happen automatically on container startup (Dockerfile), or can be run manually via Cloud SQL Proxy

⚠️ **Scaling** - Cloud Run auto-scales from 1 to 10 instances based on traffic

## Security Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Generate new `SECRET_KEY`
- [ ] Generate new `COOKIE_SECRET`
- [ ] Use Google Secret Manager for sensitive values
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Set proper `CSRF_TRUSTED_ORIGINS`
- [ ] Use HTTPS only (Cloud Run does this by default)
- [ ] Restrict CORS origins to your frontend domain

## Support Files Location
```
backend/
├── GCP_DEPLOYMENT.md              ← Detailed guide
├── GCP_DEPLOYMENT_CHECKLIST.md    ← Quick checklist
├── GCP_VALUES_REFERENCE.md        ← Value tracker
├── deploy-to-gcp.sh               ← Auto deploy script
├── .env.example                   ← Environment template
├── app.yaml                       ← App Engine config
├── Dockerfile                     ← Updated for Cloud Run
├── requirements.txt               ← Updated with GCP deps
└── anwesha/
    ├── settings.py                ← GCP configuration
    └── storage_backend.py         ← GCS support
```

## Cost Estimation (Monthly)
- Cloud SQL (db-f1-micro): ~$9
- Cloud Run: ~$5-15 (depending on traffic)
- Cloud Storage: ~$0-5 (depending on file size)
- **Total: $15-30/month** for low traffic

## Next Steps
1. Read `GCP_DEPLOYMENT.md` carefully
2. Set up GCP infrastructure (Cloud SQL, Cloud Storage, Service Account)
3. Copy `.env.example` to `.env` and fill in values
4. Run `bash deploy-to-gcp.sh` to deploy
5. Follow post-deployment steps from the guide
6. Test everything

Good luck! 🚀
