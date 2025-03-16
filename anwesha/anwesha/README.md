# Anwesha - Backend

## What is this ❓
This is the main application that wraps all the other specific applications into a single backend

### General Instructions on folder structure 📂
- `backends.py` contain EmailBackend for creating a Custom EmailBackend that will be used to establish a SMTP server with custom properties
- `prod_settings.py` contains the settings of the production deployment, such as installed apps, middlewares, databases, AWS credentials and storage settings, SMTP configurations etc
- `settings.py` is the Django application settings for development purpose, contains the same attributes as production settings
- `storage_backend.py` contains custom S3Boto3Storage classes for various storage use cases of the Anwesha app, such Profile Images, Static files, Public QR codes, Gallery storage and Multicity storage
- `urls.py` defines all the api route groups that are to be used to access the routes in the other apps

## API reference

### URL: `/admin/`
- **Description:** Provides the admin interface for managing the project. Accessible only to admin users.

---

### URL: `/user/`
- **Description:** Manages user-related operations such as authentication, registration, profile management, etc.
- **Includes:** `user.urls`

---

### URL: `/event/`
- **Description:** Handles events-related functionalities like viewing events, registering participants, payment, updating event entry etc
- **Includes:** `event.urls`

---

### URL: `/sponsors/`
- **Description:** Manages sponsor information for the event
- **Includes:** `sponsor.urls`

---

### URL: `/campasambassador/`
- **Description:** Handles campus ambassador-related features, such as ambassador login, register, logout, leaderboard information.
- **Includes:** `campus_ambassador.urls`

---

### URL: `/accounts/`
- **Description:** Provides user authentication functionality such as login, registration, password reset, etc.
- **Includes:** `allauth.urls`
  - Uses `django-allauth` for authentication, including social authentication (e.g., Google, Facebook login).

---

### URL: `/map/`
- **Description:** Provides maps and location-based services for the event, such as venue locations or interactive maps.
- **Includes:** `map.urls`

---

### URL: `/multicity/`
- **Description:** Handles city-specific event data, managing multiple locations for different cities.
- **Includes:** `multicity.urls`

---

### URL: `/atompay/`
- **Description:** Provides payment functionality using AtomPay integration.
- **Endpoints:**
  - **`/payview/`** - Handles payment processing view (Payment Initiation)
  
---

### URL: `/festpasses/`
- **Description:** Manages fest passes (ticketing) for the event. Allows the user to purchase, view, and manage event tickets.
- **Includes:** `festpasses.urls`

---

### URL: `/response/`
- **Description:** Handles AtomPay payment responses (e.g., payment success/failure callback).

---

### URL: `/slick/`
- **Description:** A custom integration for the Sleek dashboard or features related to the `sleek` app.
- **Includes:** `sleek.urls`

---

### URL: `/jet/`
- **Description:** Provides access to the Jet admin interface.
- **Includes:** `jet.urls`
  
### URL: `/jet/dashboard/`
- **Description:** Provides access to the Jet dashboard interface.
- **Includes:** `jet.dashboard.urls`

---

### URL: `/media/`
- **Description:** Serves static media files (images, videos, documents, etc.).
- **Uses:** `settings.MEDIA_URL` for file serving and `settings.MEDIA_ROOT` for file location.

## Note

For further details of the API reference, kindly go through the individual documentation of an individual application