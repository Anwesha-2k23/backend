# Multicity-app 🔢

## What is this ❓
This Application contains all the code related to Multicity events and participants.

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- `app.py` is for application specific configurations

### Configuration guidelines ⚙️
- The application uses a custom storage backend `MultiCityStorage` for storing event posters in `event_poster`.
- The createId utility is used to automatically generate unique event IDs for the `Multicity_Events` model.

## Data models 💾
- This applications contains two data models that is for the event and participant table, its feilds are a follows :-

   #### Multicity_Events

   ```
   Model representing a Multicity event.

    Attributes:
        event_id (str): Unique identifier for the event (max 4 characters).
        event_name (str): The name of the event (primary key).
        event_description (str): A description of the event (default: "description coming soon...").
        event_poster (ImageField): An image representing the event's poster, stored using the custom storage backend.
        event_date (DateTimeField): The scheduled date and time for the event.
   ```

   #### Multicity_Participants

   ```
   Model representing a Multicity event.

    Attributes:
        registration_id (str): Unique registration identifier (primary key).
        event_id (ForeignKey): Foreign key linking to the Multicity_Events model, representing the event the participant is registered for.
        payment_done (bool): Indicates whether the participant has made the required payment (default: False).
        organisation_type (str): The type of organisation the participant belongs to (choices: school, college, other).
        solo_team (bool): Indicates if the participant is part of a solo registration (default: True).
        Leader Details:
        leader_name (str): Name of the team leader.
        leader_email (str): Email address of the team leader.
        leader_phone_no (str): Phone number of the team leader.
        leader_organisation (str): Organisation of the team leader.
        Member Details (Optional):
        member_one_name (str): Name of the first member (if applicable).
        member_one_email (str): Email of the first member.
        member_one_phone_no (str): Phone number of the first member.
        member_one_organisation (str): Organisation of the first member.
        member_two_name (str): Name of the second member (if applicable).
        member_two_email (str): Email of the second member.
        member_two_phone_no (str): Phone number of the second member.
        member_two_organisation (str): Organisation of the second member.
        member_three_name (str): Name of the third member (if applicable).
        member_three_email (str): Email of the third member.
        member_three_phone_no (str): Phone number of the third member.
        member_three_organisation (str): Organisation of the third member.
   ```


## API Reference

### This application contains following api endpoints
### 1) **POST** `/register`
- This API allows users to register for an event, either as an individual (solo registration) or as part of a team.
- The request requires details such as:
    - event_id: The ID of the event to register for.
    - organisation_type: The type of the organisation (0 for School, 1 for College, 2 for Others).
    - solo_team: Whether the registration is solo (true) or a team (false).
    - leader_name, leader_email, leader_phone_no, leader_organisation: Information about the team leader.
    - member_one_name, member_one_email, member_one_phone_no, member_one_organisation: Optional fields for additional team members. The same detail is asked about member_two and member_three
- The API checks if the event exists and ensures that emails and phone numbers are valid before proceeding with the registration.
- If successful, a unique registration_id is generated and returned in the response.

