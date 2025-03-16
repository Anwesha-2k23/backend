# Atompay-Integration-App 💸

## What is this ❓
This Application contains all the code related to Atompay APIs and data.

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- middleware related code should go in `middle.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- `app.py` is for application specific configurations

### Configuration guidelines ⚙️
- This application interacts with the AtomPay API and processes responses via a secure endpoint.
- For security, encryption is handled using AES encryption for the data sent to AtomPay, and HMAC SHA-512 is used for signature validation.
- Ensure the required AtomPay keys and secrets are configured in the settings for successful communication with AtomPay.
- The system uses JWT tokens for user authentication, so the middleware must be correctly configured to validate user tokens.

## Data models 💾
- This applications only contains one data model that is for the sponsor table, its feilds are a follows :-

   ```    
    Model representing a Payment.

    Attributes:
        anwesha_id (foreign key): One-to-one relation to the `User` model, identifying the user who made the payment.
        email_id (str): Email address of the user.
        name (str): Name of the user.
        event_id (foreign key): The event for which the payment was made.
        event_type (str): Type of event (e.g., 'solo', 'team').
        atompay_transaction_id (str): The transaction ID from AtomPay.
        bank_transaction_id (str): The bank transaction ID from the payment gateway.
        payment_status (str): The status of the payment (e.g., 'success', 'failed').
   ```


## API Reference

### This application contains following api endpoints
### 1) **POST** `/atompay`
- This API is used to initiate the payment process. It accepts payment details from the user and interacts with the AtomPay payment gateway.

### 2) **POST** `/response`
- This API handles the response from AtomPay after the payment has been completed. It processes the payment details, checks for transaction validity, and updates the payment status in the system.
