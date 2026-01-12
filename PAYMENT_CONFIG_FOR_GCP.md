# Payment Configuration for GCP Deployment

## Atom Pay Configuration

### Current Settings (Local)
```python
# anwesha/atompay/views.py - Line 61
returnUrl = 'http://127.0.0.1:8000/response/'

# anwesha/settings.py
ATOM_MERCHANT_ID = '564719'
ATOM_MERCHANT_PASSWORD = 'anwesha@24'
ATOM_RETURN_URL = 'http://127.0.0.1:8000/response/'
```

### For Production (Cloud Run)
You need to change these to your Cloud Run domain:

**Example:**
If your Cloud Run service URL is: `https://anwesha-backend-abc123.run.app`

Then update:
```python
# anwesha/atompay/views.py - Line 61
returnUrl = 'https://anwesha-backend-abc123.run.app/response/'

# .env
ATOM_RETURN_URL=https://anwesha-backend-abc123.run.app/response/
```

## Steps to Update Payment Config

### 1. After Cloud Run Deployment
Once you deploy to Cloud Run, you'll get a URL like:
```
https://anwesha-backend-XXXXX.run.app
```

### 2. Update These Files

**Option A: Using Environment Variables (Recommended)**
```bash
# In .env file
ATOM_RETURN_URL=https://anwesha-backend-XXXXX.run.app/response/
```

**Option B: Direct Code Change (Not Recommended)**
Edit `anwesha/atompay/views.py` line 61:
```python
# Change from:
returnUrl = 'http://127.0.0.1:8000/response/'

# To:
returnUrl = 'https://anwesha-backend-XXXXX.run.app/response/'
```

Then rebuild and redeploy Docker image.

### 3. Update in Atom Merchant Dashboard

If you have configured Atom's hosted payment page:
1. Log in to Atom merchant dashboard
2. Update "Return URL" / "Success URL" to: `https://anwesha-backend-XXXXX.run.app/response/`
3. Update "Failure URL" to: `https://anwesha-backend-XXXXX.run.app/response/` (same endpoint handles both)

## Payment Flow Architecture

```
1. User initiates payment on frontend
   ↓
2. Frontend calls: POST https://anwesha-backend-XXXXX.run.app/atompay/
   (with JWT token, event_id, amount, type, etc.)
   ↓
3. Backend generates Atom Token & returns response with atomTokenId
   ↓
4. Frontend submits form to Atom's hosted checkout:
   POST https://paynetzuat.atomtech.in/paynetz/epi/fts
   (with atomTokenId, merchId, returnUrl, etc.)
   ↓
5. User completes payment on Atom's page
   ↓
6. Atom redirects to: POST https://anwesha-backend-XXXXX.run.app/response/
   (with encrypted encData)
   ↓
7. Backend decrypts, validates signature, creates SoloParticipants/Team payment record
   ↓
8. Returns response.html with payment confirmation
```

## Key Endpoints

### Local Development
- Token Generation: `POST http://127.0.0.1:8000/atompay/`
- Payment Callback: `POST http://127.0.0.1:8000/response/`

### Production (Cloud Run)
- Token Generation: `POST https://anwesha-backend-XXXXX.run.app/atompay/`
- Payment Callback: `POST https://anwesha-backend-XXXXX.run.app/response/`

## Testing Payment in Production

### 1. Get Atom Token
```bash
curl -X POST https://anwesha-backend-XXXXX.run.app/atompay/ \
  -H "Content-Type: application/json" \
  -b "jwt=YOUR_JWT_TOKEN" \
  -d '{
    "event_id": "1",
    "amount": "100",
    "email": "test@example.com",
    "phone": "9876543210",
    "type": "solo",
    "anwesha_id": "ANWESHA_ID"
  }'
```

Expected Response:
```json
{
  "atomTokenId": "15000036573256",
  "merchId": "564719",
  "custEmail": "test@example.com",
  "custMobile": "9876543210",
  "returnUrl": "https://anwesha-backend-XXXXX.run.app/response/",
  "amount": "100",
  "merchTxnId": "abc123def456"
}
```

### 2. Submit to Atom Payment Page
Create a form and submit to Atom's endpoint with the token received above.

### 3. Verify Callback
After payment, check Cloud Run logs to see if callback was received:
```bash
gcloud run logs read anwesha-backend --region=asia-south1 --limit=50
```

## Environment Variable for Payment

Add to `.env.example` and `.env`:
```env
# Payment (Atom Pay)
ATOM_MERCHANT_ID=564719
ATOM_MERCHANT_PASSWORD=anwesha@24
ATOM_RETURN_URL=https://anwesha-backend-XXXXX.run.app/response/
```

## Razorpay (Currently Unused)
Currently, Razorpay integration code exists but is not used. The active payment system is **Atom Pay**.

If you want to enable Razorpay in the future:
```env
RAZORPAY_API_KEY_ID=your_key
RAZORPAY_API_KEY_SECRET=your_secret
```

## Important Notes

⚠️ **HTTPS Required** - Atom Pay requires HTTPS for return URLs. Cloud Run provides HTTPS by default.

⚠️ **Update Order Matters** - Update `.env` first, then rebuild Docker if you changed it, then redeploy.

⚠️ **Test Thoroughly** - Always test payment flow in GCP Cloud Run before going live.

⚠️ **Endpoint Security** - The `/response/` endpoint is CSRF-exempt (required for Atom's callback). Make sure it validates payment signature properly.

## Sandbox vs Production

### Sandbox (For Testing)
- Atom Endpoint: `https://paynetzuat.atomtech.in/...`
- Merchant ID: `564719` (test account)
- Can test without real payments

### Production (When Live)
- Atom Endpoint: `https://payment1.atomtech.in/...` or Atom's production URL
- Merchant ID: Your production account ID
- Real payments required

## Migrating from Local to Production

```bash
# 1. Get Cloud Run URL after deployment
gcloud run services describe anwesha-backend --region=asia-south1 --format='value(status.url)'

# 2. Update .env with the URL
ATOM_RETURN_URL=https://anwesha-backend-XXXXX.run.app/response/

# 3. If you hardcoded in views.py, update and rebuild:
# Edit anwesha/atompay/views.py line 61
# Rebuild: docker build -t gcr.io/anwesha-26-472317/anwesha-backend:latest .
# Push: docker push gcr.io/anwesha-26-472317/anwesha-backend:latest
# Redeploy: gcloud run deploy anwesha-backend --image=... --region=asia-south1

# 4. Test payment flow
```

## Troubleshooting Payment Issues

**"Invalid return URL" error from Atom:**
- Check if ATOM_RETURN_URL is correct
- Verify it's HTTPS
- Check if it matches Atom's merchant dashboard settings

**"Callback not received" error:**
- Check Cloud Run logs for 404 errors
- Verify `/response/` endpoint is accessible
- Check if CSRF exemption is still in place

**"Payment successful but not registered":**
- Check database - look at Payments table
- Check if SoloParticipants/Team record was created
- Verify signature validation passed in logs

## Support Files
- [GCP_DEPLOYMENT.md](GCP_DEPLOYMENT.md) - Full deployment guide
- [GCP_VALUES_REFERENCE.md](GCP_VALUES_REFERENCE.md) - All values to track
- [GCP_DEPLOYMENT_CHECKLIST.md](GCP_DEPLOYMENT_CHECKLIST.md) - Pre-deployment checklist
