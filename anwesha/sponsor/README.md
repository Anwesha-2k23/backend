#  Sponser-App 💸

## What is this ❓
This Application contains all the code related to Sponsor APIs and data.

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- middleware related code should go in `middle.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- `app.py` is for application specific configurations

### Configuration guidelines ⚙️
- Sponsor app is not directly connected to S3 folders so to connectect it use boto S3 and make required changes in `sponsor_logo` field in `models.py`

## Data models 💾
- This applications only contains one data model that is for the sponsor table, its feilds are a follows :-

   ```
   Model representing a Sponsor.

    Attributes:
        sponsor_name (str): Name of the sponsor (Max 50 characters)
        sponsor_phone_number (str): Phone number of the sponsor (Max 15 characters)
        sponsor_description (str): Description of the sponsor (optional)
        order (number): Order in which the sponsors are displayed (default: 0)
        sponsor_email (str): Email address of the sponsor (unique)
        sponsor_logo (Img): Sponsor's logo image
        sponsor_link (str): Website link of the sponsor (optional)
        sponsor_instagram_id (str): Instagram ID of the sponsor (optional)
        sponsor_facebook_id (str): Facebook ID of the sponsor (optional)
        sponsor_linkdin_id (str): LinkedIn ID of the sponsor (optional)
   ```


## API Reference

### This application contains following api endpoints
### 1) **GET** `/allsponsors`
- This api will give the list of all sponsors in the oder decribed and all the information regarding them.

