# GCP Deployment - Quick Reference Card

## One-Liner Deployment (After Setup)
```bash
bash deploy-to-gcp.sh
```

## Essential Commands

### Setup (One-time)
```bash
# Authenticate with GCP
gcloud auth login
gcloud config set project anwesha-26-472317

# Create Cloud SQL
gcloud sql instances create anwesha-mysql --database-version=MYSQL_8_0 --tier=db-f1-micro --region=asia-south1
gcloud sql databases create anwesha_db --instance=anwesha-mysql
gcloud sql users create anwesha_user --instance=anwesha-mysql --password=YOUR_PASSWORD

# Create bucket
gsutil mb -l asia-south1 gs://anwesha-storage-bucket

# Create service account
gcloud iam service-accounts create anwesha-service --display-name="Anwesha Backend"
```

### Build & Deploy
```bash
# Build Docker image
docker build -t gcr.io/anwesha-26-472317/anwesha-backend:latest .

# Push to GCR
docker push gcr.io/anwesha-26-472317/anwesha-backend:latest

# Deploy to Cloud Run
gcloud run deploy anwesha-backend \
  --image=gcr.io/anwesha-26-472317/anwesha-backend:latest \
  --region=asia-south1 \
  --service-account=anwesha-service@anwesha-26-472317.iam.gserviceaccount.com \
  --add-cloudsql-instances=anwesha-26-472317:asia-south1:anwesha-mysql
```

### Migrations & Setup
```bash
# Run migrations (using Cloud SQL Proxy)
./cloud_sql_proxy -instances=anwesha-26-472317:asia-south1:anwesha-mysql=tcp:3306 &
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

### Monitoring
```bash
# View logs
gcloud run logs read anwesha-backend --region=asia-south1 --limit=50

# Check service status
gcloud run services describe anwesha-backend --region=asia-south1

# Get service URL
gcloud run services describe anwesha-backend --region=asia-south1 --format='value(status.url)'
```

### Troubleshooting
```bash
# SSH into running container (if needed)
gcloud run execute anwesha-backend --command="bash"

# View Cloud SQL logs
gcloud sql operations list --instance=anwesha-mysql

# Check bucket contents
gsutil ls gs://anwesha-storage-bucket/

# Test database connection (locally via proxy)
mysql -h 127.0.0.1 -u anwesha_user -p -D anwesha_db
```

---

## Configuration Checklist

```
GCP Setup
├─ Project ID: anwesha-26-472317
├─ Region: asia-south1
├─ Cloud SQL instance: anwesha-mysql
├─ Cloud Storage bucket: anwesha-storage-bucket
└─ Service account: anwesha-service@...

Database
├─ Instance: anwesha-mysql
├─ Database: anwesha_db
├─ User: anwesha_user
└─ Password: [CREATE IN GCP]

Docker & Registry
├─ Image: gcr.io/anwesha-26-472317/anwesha-backend
├─ Authenticated: gcloud auth configure-docker ✓
└─ Pushed: docker push ✓

Cloud Run Service
├─ Name: anwesha-backend
├─ Region: asia-south1
├─ Memory: 512Mi
├─ CPU: 1
├─ Min instances: 1
├─ Max instances: 10
└─ URL: anwesha-backend-XXXXX.run.app

Environment Variables
├─ CONFIGURATION=gcp ✓
├─ DEBUG=False ✓
├─ SECRET_KEY=[NEW] ✓
├─ CLOUD_SQL_CONNECTION_NAME=anwesha-26-472317:asia-south1:anwesha-mysql ✓
├─ DB_PASSWORD=[CREATED] ✓
├─ GCP_STORAGE_ENABLED=True ✓
└─ [Other variables filled in .env]
```

---

## Files & Locations

| File | Purpose | Status |
|------|---------|--------|
| `anwesha/settings.py` | Django config for GCP | ✅ Updated |
| `Dockerfile` | Container image | ✅ Updated |
| `requirements.txt` | Python dependencies | ✅ Updated |
| `anwesha/storage_backend.py` | GCS integration | ✅ Updated |
| `.env.example` | Environment template | ✅ Created |
| `app.yaml` | App Engine config | ✅ Created |
| `GCP_DEPLOYMENT.md` | Detailed guide | ✅ Created |
| `GCP_DEPLOYMENT_CHECKLIST.md` | Pre-flight checks | ✅ Created |
| `GCP_VALUES_REFERENCE.md` | Value tracker | ✅ Created |
| `PAYMENT_CONFIG_FOR_GCP.md` | Payment setup | ✅ Created |
| `GCP_ARCHITECTURE_GUIDE.md` | Visual architecture | ✅ Created |
| `deploy-to-gcp.sh` | Auto-deploy script | ✅ Created |

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `403 Permission denied` | Run: `gcloud auth login` and check service account permissions |
| `Cloud SQL connection failed` | Ensure Cloud SQL Admin API is enabled and proxy is running |
| `Static files not found` | Run: `python manage.py collectstatic --noinput` |
| `DEBUG=True errors in production` | Set `DEBUG=False` in `.env` |
| `CORS errors from frontend` | Update `CORS_ALLOWED_ORIGINS` with frontend domain |
| `Payment callback not received` | Check if `/response/` is accessible and ATOM_RETURN_URL is correct |

---

## Important Reminders

⚠️ **Never commit `.env` to Git** - Use `.env.example` only

⚠️ **Change SECRET_KEY for production** - Generate a new strong key

⚠️ **Use Google Secret Manager** for sensitive values

⚠️ **Set DEBUG=False** for production

⚠️ **Update ATOM_RETURN_URL** with Cloud Run domain after deployment

⚠️ **Test payment flow** thoroughly before going live

⚠️ **Monitor costs** - Cloud SQL and Cloud Storage have storage charges

⚠️ **Set up backups** for Cloud SQL database

⚠️ **Use HTTPS only** (Cloud Run provides this by default)

---

## Support Documentation

| Document | Contains |
|----------|----------|
| `GCP_DEPLOYMENT.md` | Step-by-step setup guide |
| `GCP_DEPLOYMENT_CHECKLIST.md` | Before/during/after checklist |
| `GCP_ARCHITECTURE_GUIDE.md` | Visual diagrams & flows |
| `GCP_VALUES_REFERENCE.md` | All GCP resource values |
| `PAYMENT_CONFIG_FOR_GCP.md` | Payment configuration |

---

## Next Steps

1. Read `GCP_DEPLOYMENT.md` completely
2. Set up GCP infrastructure (Cloud SQL, Storage, Service Account)
3. Copy `.env.example` → `.env` and fill in values
4. Run `bash deploy-to-gcp.sh`
5. Run migrations via Cloud SQL Proxy
6. Test API endpoints
7. Update frontend URLs
8. Test payment flow
9. Monitor logs and costs

---

**Your backend is ready for GCP Cloud Run deployment! 🚀**

For detailed steps, see: `GCP_DEPLOYMENT.md`
