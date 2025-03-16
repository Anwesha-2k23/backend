#  Slick-App 🔥

## What is this ❓
This Application contains all the code related to Slick registration

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- `app.py` is for application specific configurations

### Configuration guidelines ⚙️
- The only configuration required is a token, as the API endpoint is based on token-based authorization

## Data models 💾
- This applications does not contain a model as such, but as per the API endpoint, the model is :-

   ```
   Model representing a slick registration.

    Attributes:
        anwesha_id (str): Unique ID assigned to the user.
        full_name (str): Full name of the user.
        email_id (str): Email address of the user (unique).
        phone_number (str): User’s phone number.
        college_name (str): Name of the college (if applicable).
        user_type (str): Type of user (e.g., "student", "iitp_student", "non-student", etc.).
        password (str): Password for the user account (defaults to email).
        is_email_verified (bool): Whether the email is verified (default: True).
   ```


## API Reference

### This application contains following api endpoints
### 1) **POST** `/register`
- Register a new slick user or returns the existing user's Anwesha ID if user already exists.
  
  #### Request
  ```json
  {
    "email_id": "johndoe@email.com",
    "full_name": "John Doe",
    "phone_number": "9876543210",
    "college_name": "IIT Patna",
    "user_type": "iitp_student",
    "token": "AnweshaIitpxSlick"
  }
  ```

  #### Response
  ```json
    {
    "Anwesha_id": "ANWXXXXXX"
    }
  ```


