#  CA-App 🎓

## What is this ❓
This Application contains all the code related to Campus Ambassador APIs and data.

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- `app.py` is for application specific configurations
- `management/commands` contains the commands for loading CA data into the database

### Configuration guidelines ⚙️
- Sponsor app is not directly connected to S3 folders so to connectect it use boto S3 and make required changes in `sponsor_logo` field in `models.py`

## Data models 💾
- This applications has one model :-

   ```
    Attributes:

    ca_id = A unique identifier for the campus ambassador. It's used as the primary key for identifying the ambassador in the system.
    anwesha = A foreign key that links the campus ambassador to a specific user in the User model. This connects the ambassador's data to their user account.
    password = The hashed password of the campus ambassador used for authentication. It ensures secure login for the ambassador.
    phone_number = The phone number of the campus ambassador. This is used for contact and verification purposes.
    email_id = The email address of the campus ambassador. It is used for communication and is required for login. It must be unique within the system.
    full_name = The full name of the campus ambassador. This is used for displaying the ambassador’s name across the platform.
    college_name = The name of the college that the ambassador represents. It helps identify the ambassador’s affiliation.
    college_city = The city where the ambassador's college is located. This is an optional field but adds geographical context to the ambassador's profile.
    refferal_code = A referral code generated for each campus ambassador. This can be used for tracking referrals made by the ambassador to the platform.
    age = The age of the campus ambassador. This is used to understand the demographics of the ambassadors.
    intrests = The specific interests of the campus ambassador. It is an optional field where the ambassador can select their areas of interest from predefined choices (e.g., "Interest 1", "Interest 2", "Interest 3").
    gender = Description: The gender of the campus ambassador. This is an optional field and can be one of several predefined choices (Male, Female, Rather not say, Others).
    score = The accumulated score of the campus ambassador, which could be based on their activities, participation, or achievements on the platform.
    is_loggedin = A boolean field indicating whether the campus ambassador is currently logged in to the platform. This helps in managing sessions.
    validation = A boolean field indicating whether the campus ambassador's email has been verified. If True, the ambassador's email is validated and they can proceed to use the platform.
    instagram_id = The Instagram handle or ID of the campus ambassador, if they choose to share it. This is used for integrating the ambassador's social media presence.
    facebook_id = The Facebook handle or ID of the campus ambassador, if they choose to share it. This helps connect the ambassador’s social presence to the platform.
    linkdin_id = The LinkedIn ID or profile link of the campus ambassador, if provided. This connects the ambassador’s professional network to the platform.
    twitter_id = The Twitter handle of the campus ambassador, if shared. This is another way to link the ambassador’s social media profiles with the platform.
    date_of_birth = The birth date of the campus ambassador. This field is optional but can be used for demographic analysis.
    time_of_registration = The profile picture of the campus ambassador. This image is stored and managed via a custom storage backend (`ProfileImageStorage), allowing the ambassador to upload and display their photo.
   ```


## API Reference

### This application contains following api endpoints
### 1) **GET** `/allcampusambassadors`
- This API returns a list of all campus ambassadors with their `anwesha`, `email_id`, `full_name`, and `college_name`.

### 2) **POST** `/register`
- This API registers a new campus ambassador.

### 3) **POST** `/login`
- This API logs in a campus ambassador by checking the provided credentials.

### 4) **POST** `/logout`
- This API logs out a campus ambassador by clearing their session (JWT).

### 5) **GET** `/leaderboarddata`
- This API fetches the leaderboard sorted by `score`.

### 6) **GET/POST** `/editprofile`
- Retrieves or updates the campus ambassador's profile. GET method fetches the details of the logged-in user while POST method updates it
  
### 7) **POST** `/verifyemail`
- This API verifies the email address for a campus ambassador.

### 8) **GET** `/verifyemail/token`
- This API verifies the email using the token. This token may be obtained from `/verifyemail`