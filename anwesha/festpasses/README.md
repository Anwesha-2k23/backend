#  Festpasses-App 🎟️

## What is this ❓
This application handles the management of fest passes, including registration, payment status, and entry validation. Users can register for fest passes, check their payment and entry status, and complete transactions.

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- `app.py` is for application specific configurations

### Configuration guidelines ⚙️
- Ensure that the `payment_done` and `has_entered` fields are properly set based on the user's transaction status and event entry.

## Data models 💾
- This applications only contains one data model that is for the festpasses table, its feilds are a follows :-

   ```
    Model representing a FestPass.

    Attributes:
        anwesha_id (foreign key): One-to-one relation to the `User` model. Unique to each user.
        email_id (str): Email address of the user (unique).
        transaction_id (str): Unique transaction ID associated with the payment.
        has_entered (bool): Whether the user has entered the event (default: False).
        payment_done (bool): Whether the payment for the fest pass has been successfully completed (default: False).

   ```


## API Reference

### This application contains following api endpoints
### 1) **POST** `/register`
- This endpoint allows users to register for a fest pass. It checks if the user is already registered and if payment has been done.

### 2) **POST** `/getStatus`
- This API will return the status of the fest pass for a given user, including entry and payment status, based on the `anwesha_id` of the user.

### 3) **POST** `/setStatus`
- This API updates the entry status of a user, marking them as having entered the event.

### 4) **POST** `/get`
- This API checks if a user is registered for the fest pass by verifying their anwesha_id.

### 5) **POST** `/atompay`
- This endpoint processes the payment for the fest pass using AtomPay. It generates a unique transaction ID and returns the payment URL for completing the transaction.

### 6) **POST** `/response`
- This endpoint receives the payment response from AtomPay. It processes the payment details and validates the transaction. If successful, it creates a fest pass entry for the user.


