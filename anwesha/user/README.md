#  User-App

## What is this ❓
This Application contains all the code related to user authenticaton and QR regenration.

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- middleware related code should go in `middle.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- Code must follow DRY principle and all the utlilty functions should go in `utility.py`
- `app.py` is for application specific configurations

### Configuration guidelines ⚙️

- In this application only configuration required is when you want to store your images and QR to AWS S3 , then you need to change QR and profilePitcure field in  `models.py`
- In views.py there is not a feature to switch between S3 qr url and static storage url so  thats needs to be handled manually
- verifyEmail Api in `views.py` has a redirect url that needs to point to your frontend application.

## Data models 💾
- This applications only contains one data model that is for the user table, its feilds are a follows :-

   ```
   Model representing a User.

    Attributes:
        User_type_choice (Enum): Enum class for user types.
        Gender (Enum): Enum class for gender options.
        anwesha_id (str): Anwesha ID of the user.
        password (str): Hashed password of the user.
        phone_number (str): Phone number of the user.
        email_id (str): Email ID of the user.
        full_name (str): Full name of the user.
        collage_name (str): Name of the college of the user.
        age (int): Age of the user.
        is_email_verified (bool): Indicates if the user's email is verified or not.
        user_type (str): Type of the user (choices from User_type_choice).
        gender (str): Gender of the user (choices from Gender).
        accomadation_selected (bool): Indicates if the user has selected accommodation.
        is_profile_completed (bool): Indicates if the user has completed their profile.
        instagram_id (str): Instagram ID of the user.
        facebook_id (str): Facebook ID of the user.
        time_of_registration (datetime): Timestamp of user registration.
        is_locked (bool): Indicates if the user is locked.
        is_loggedin (bool): Indicates if the user is logged in.
        profile (ImageField): Image field for the user's profile.
        profile_photo (ImageField): Image field for the user's profile photo (storage settings based on configuration).
        qr_code (ImageField): Image field for the user's QR code (storage settings based on configuration).
        signature (str): Signature of the user which is used in QR code.
        secret (str): randomly generated string for adding in signature for qr identification.
   ```


## API Reference

### This application contains following api endpoints
### 1) **GET** `/login`
- This api is used for login directly if a user has jwt cookie saved, also this api checks if email is verified or not.
- To allow user entry a cookie named  `jwt` shiuld be present in headers and value of cookie should be a jwt cookie set by login post api.

### 2) **POST** `/login`
- This api is used for login using email address/anwesha ID and password and will save a cookie.

```
Required Attributes:-

{
    "username": <-- email address or anwesha ID of user -->,
    "password": <-- password of user -->,
}
```

### 3) **POST** `/logout`
- This api will delete the stored cookie and change flags to make the user offline
- Important thing to note is is that this is a POST request which takes no inputs

### 4) **POST** `/register`
- This api is used to create user and save them in database.
- This api will create user but they will not able to login until they verify their email using `/verifyemail` api.
- only compulsary fields will be allowed here other fields can be changed by `/editprofile`

```
Required Attributes:-

{
    "email_id": <-- email address of user , this will be a unique field -->,
    "password": <-- password -->,
    "full_name": <-- full name -->,
    "phone_number": <--phone number, this will be a unique field  -->,
    "college_name": <-- college name of user-->,
    "user_type" : <-- this can have 5 possible string values , [iitp_student,student,non-student,alumni,faculty] -->,
}
```
### 5) **POST** `/editprofile` 🔒 *Protected-route*
- This api is used  to change any field in data base except unique fields.

```
Allowed fields:
    full_name
    phone_number
    college_name
    age
    gender
    instagram_id
    facebook_id
    profile_photo : (image field)
```
### 6) **GET** `/editprofile` 🔒 *Protected-route*
- This api provides all the data of an user in json object.

```
sample response
{
    "anwesha_id": <--string-->,
    "full_name": <--string-->,
    "phone_number": <--string-->,
    "email_id": <--string-->,
    "college_name": <--string-->,
    "age": <--number-->,
    "is_email_verified": <--boolean-->,
    "gender": <--string-->,
    "is_profile_completed": <--boolean-->,
    "profile_picture": <--string-->,
    "user_type": <--string-->,
    "qr_code": <-- S3 url will be returned-->
}
```

### 7) **POST** `/verifyemail`
- This api takes an email address as an input and sends email with verification link to that email only if email exist in database.

```
Required fields
{
    "email":<--email must be registered-->
}
```
### 8) **GET** `/verifyemail/<str>`
- This api will check the html parameter str and verify wheter its generated by backend and verify email of the user accordingly

### 9) **POST** `/forgetpassword`
- This api will take email as input and check if  it exists in database and if it does will generate and send a pass word token to using email service
```
Required fields
{
    "email":<--email must be registered-->
}
```

### 10) **GET** `regenerateqr` 🔒  *Protected-route*
- This api is to regenerate the QR code and will return the S3 link  to the regenerated QR

