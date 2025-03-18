# Event-App 🎉

## What is this ❓
This Application contains all the code related to Event APIs and data.

### General Instructions on file structure 📂
- code for Api are in `views.py` where each class maps to an api endpoint.
- data model of user object in `models.py`
- admin pannel configurations are in `admin.py`
- all the test should be in `test.py`
- `app.py` is for application specific configurations

### Configuration guidelines ⚙️
- Razorpay and PayU payment gateways are used. Ensure that the respective API keys are set up as environment variables.
- Configure the webhook URLs and API keys for Razorpay and PayU in the settings.
- Environment variables should be set up to securely store API keys (`RAZORPAY_API_KEY_ID`, `RAZORPAY_API_KEY_SECRET`, `PAYU_API_KEY`, `PAYU_API_SECRET`).
- The application uses JWT tokens for authentication, which are handled via the Autherize decorator.

## Data models 💾
- This applications only contains the following data models that is for the event table, its feilds are a follows :-

   ```
    Model representing Gallery with image content

    Attributes:
        name (str): The name of the Gallery content.
        file (File): The file that will be stored in `/static/gallery`
        type (str): Choice between "image" or "video"
        tags: A selection of tags such tech, cultural, sports, gaming etc
        timestamp (datetime): The time when the gallery content was uploaded


    Model representing an Event

    Attributes:
        id (str): A unique identifier for the event. It is a string field, with a maximum length of 10 characters. The ID is automatically generated using a function (createId) when the event is saved, ensuring that every event has a unique ID. This field is also the primary key for the model.
        name (str): The name of the event. This is a required field with a maximum length of 100 characters.
        organizer (str): The name of the entity organizing the event. This is a required field with a maximum length of 100 characters.
        venue (str): The location where the event will take place. This field has a maximum length of 255 characters.
        description (str): A detailed description of the event. This can be a longer text providing more context about what the event entails.
        start_time (DateTime): The start date and time of the event. This is an optional field and can be left blank if not applicable.
        end_time (DateTime): The end date and time of the event. Similar to start_time, this is an optional field.
        prize (str): A description of the prize(s) that will be awarded during the event. The maximum length is 150 characters, and the default value is "0", which likely represents no prize.
        registration_fee (Decimal): The registration fee for the event. This is a decimal number, and it can store up to 8 digits with 2 decimal places. The default value is 0, indicating no fee.
        registration_deadline (DateTime): The deadline for registering for the event. This is an optional field and can be left blank if not applicable.
        video (URL): A URL linking to a video related to the event (e.g., an introduction or promotional video). This is an optional field.
        poster (URL): A URL linking to an image of the event's poster. This is also an optional field.
        tags (str): Tags related to the event, which help categorize and filter events. This field has a maximum length of 40 characters and uses predefined choices defined in the TAGS variable.
        max_team_size (smallint): The maximum number of participants allowed in a team for team-based events. The default value is set to 1, indicating individual participation unless otherwise specified.
        min_team_size (smallint): The minimum number of participants required for team events. The default value is set to 1.
        is_active (boolean): A boolean flag indicating whether the event is currently active. If set to False, the event is considered inactive and won't appear for registration. The default value is True.
        is_online (boolean): A boolean flag indicating whether the event is held online. If set to True, the event is considered an online event. The default value is False.
        registration_link (URL): A URL link to the registration page for the event. This is an optional field.
        order (IntegerField): An integer representing the order in which the event should be displayed relative to other events. The default value is 0, meaning it will appear first unless overridden.
        payment_link (URL): A URL for a payment page, if applicable. This is an optional field and can be used when there’s a fee associated with the event.
        payment_key (str): A key used for payment integration. This is an optional field and can store the key for the payment gateway used by the event.


    Model representing a Solo Participant

    Attributes:
        anwesha_id (User): User who registered.
        event_id (Event): The event the participant is registered for.
        payment_done (bool): Whether the payment has been completed.


    Model representing a Team

    Attributes:
        team_id (str): Unique ID for the team.
        event_id (Event): Event the team is registered for.
        leader_id (User): Leader of the team.
        team_name (str): Name of the team.
        payment_done (bool): Whether the payment for the team has been completed.


    Model representing a Team Participant

    Attributes:
        team_id (Team): The team the participant belongs to.
        anwesha_id (User): User who is part of the team.
        event_id (Event): The event the participant is registered for.

    
    Model representing Payer

    Attributes:
        payer_id (User): The user making the payment.
        order_id (str): The Razorpay order ID for the payment.
        payment_status (str): The payment status (e.g., PAID, UNPAID).
        datetime (datetime): Date and time when the payment was made.
        team_id (Team): The associated team (if any).
        signature (str): Razorpay payment signature for validation.
        payment_id (str): Razorpay payment ID.


    Model representing PayUTxn (PayUTransaction)

    Attributes:
        txnid (str): Unique transaction ID from PayU.
        mihpayid (str): Merchant ID for PayU.
        mode (str): Payment mode (e.g., credit card, debit card).
        key (str): API key for PayU.
        amount (float): Transaction amount.
        addedon (datetime): Date and time the transaction was made.
        productinfo (str): Information about the product or event.
        firstname (str): First name of the payer.
        email (str): Email address of the payer.
        phone (str): Phone number of the payer.
        status (str): Payment status (e.g., success, failed).
        field1 to field5 (str): Extra fields for the transaction data.
   ```

## API Reference

### This application contains following api endpoints
### 1) **GET** `/allevents`
- This API retrieves a list of all available events.

### 2) **GET** `/id/<str:event_id>`
- This API will retrieve details for a specific event using its unique `event_id`.

### 3) **GET** `/tags/<str:event_tags>`
- This API will retrieve events filtered by tags. Tags can be used to categorize events (e.g., "sports", "workshops").

### 4) **POST** `/registration/team`
- This API registers a user as the leader of a team for a team event. The leader must also provide the `anwesha_id` of the team members

### 5) **POST** `/registration/solo`
- This API registers a user for a solo event for an event with `event_id`. If no payment is required, the `payment_url` will be null. For IITP students, payment is generally not required.

### 6) **POST** `/registration/verification`
- This API verifies a payment made via Razorpay after a user completes a transaction

### 7) **GET** `/myevents`
- This API retrieves the list of events the current user has registered for.

### 8) **POST** `/payment/webhook/very/sus/api`
- This is the webhook endpoint used to receive and verify payment notifications from Razorpay or PayU

### 9) **POST** `/checkeventregistration`
- This API checks if the user has registered for a particular event.

### 10) **POST** `/updateentrystatus`
- This API updates the entry status of a user or team for an event. This could be used to mark a user's registration as confirmed or to change other related statuses.


## Webhooks

- Razorpay Webhook: Used to verify payment signatures from Razorpay and update payment statuses in the system.
- PayU Webhook: Receives and verifies payment notifications from PayU.