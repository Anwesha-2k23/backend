#  Map-App 🗺️

## What is this ❓
This Application contains all the code related to Map APIs and data.

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- `app.py` is for application specific configurations

### Configuration guidelines ⚙️
- You might need to modify storage settings for images. In models.py, the poster field in the City model currently uses a local path, but you can uncomment and modify the `MultiCityStorage` storage backend if you need cloud storage (e.g., for S3).

## Data models 💾
- This applications only contains one data model that is for the city table, its feilds are a follows :-

   ```
   Model representing a City.

   Attributes:
      city_name (str): Name of the city (Max 100 characters)
      poster (Img): Poster image for the city (optional)
      venue (str): The main venue in the city (Max 150 characters)
      date (datetime): Date of the event in the city
      contacts (json): Contact information for the city or event organizers
      register_link (url): URL for registration for events or activities
      rulebook (url): URL to the rulebook for the event
      description (str): A description of the city or event
      events (json): A list of events happening in the city

   ```


## API Reference

### This application contains following api endpoints
### 1) **GET** `/allcities`
- This API will return a list of all cities with basic information such as city name, poster, and event date.
### 2) **GET** `/{cityname}`
- This API will return detailed information about a specific city, including its venue, contacts, registration link, rulebook, description, and events.
