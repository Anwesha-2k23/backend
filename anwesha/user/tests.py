import pytest
from rest_framework.test import APIClient
from user.models import User
import jwt
from anwesha.settings import CONFIGURATION,COOKIE_ENCRYPTION_SECRET
import datetime
from django.urls import reverse

client = APIClient()

@pytest.mark.django_db
@pytest.fixture
def default_user():
    """
    
    Fixture to create a test user.
    
    """
    def _create_user(email, password,phone_number,anwesha_id="ANW0001", is_email_verified=True):
        return User.objects.create(
            email_id=email,
            password=(password),
            anwesha_id=anwesha_id,
            is_email_verified=is_email_verified,
            collage_name="XYZ",
            user_type="student",
            phone_number=phone_number
        )
    return _create_user(email="testuser@gmail.com", password="password", is_email_verified=True,phone_number="1234567890")


@pytest.mark.django_db
@pytest.fixture
def create_user():
    def _create_user(email, password,phone_number,anwesha_id="ANW0002", is_email_verified=True):
        return User.objects.create(
            email_id=email,
            password=(password),
            anwesha_id=anwesha_id,
            is_email_verified=is_email_verified,
            collage_name="XYZ",
            user_type="student",
            phone_number=phone_number
        )
    return _create_user


@pytest.fixture
def generate_token(create_user):
    def getToken(anwesha_id):
        payload = {
            "id": anwesha_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, COOKIE_ENCRYPTION_SECRET, algorithm='HS256')
        return token
    return getToken


# TEST TO CHECK USER REGISTRATION
@pytest.mark.django_db
@pytest.mark.parametrize("payload, expected_status, expected_message",[
     (
            {
                "full_name": "test1",
                "email_id": "test@gmail.com",
                "password": "password",
                "phone_number": "1234567899",
                "college_name": "XYZ",
                "user_type": "student",
            },
            '201',
            "User created successfully!",
    ),
    (
            {
                "full_name": "test2",
                "email_id": "testuser@gmail.com",
                "password": "password",
                "phone_number": "1234567889",
                "college_name": "XYZ",
                "user_type": "student",
            },
            '409',
            "A user with the same email already exists",
    ),
    (
            {
                "full_name": "test3",
                "email_id": "test3@gmail.com",
                "password": "password",
                "phone_number": "1234567890",
                "college_name": "XYZ",
                "user_type": "student",
            },
            '409',
            "A user with the same phone number already exists",
    ),
])
def test_register(default_user,payload, expected_status, expected_message):
    response = client.post("/user/register", payload)
    response_data = response.json()
    assert response_data['status'] == expected_status
    assert expected_message in response_data["message"]
    

# TEST TO CHECK USER LOGIN
@pytest.mark.django_db
def test_login_success(create_user):
    user = create_user(email="testuser@gmail.com", password="password123", is_email_verified=True,phone_number='1234567899')
    payload = {"username": user.email_id, "password":"password123"}
    response = client.post("/user/login", payload)
    response_data = response.json()
    print(response_data)
    assert User.objects.filter(email_id="testuser@gmail.com").exists()
    assert response_data['status'] == 200
    assert response_data["success"] is True
    assert response_data["anwesha_id"] == user.anwesha_id
    assert "jwt" in response.cookies


@pytest.mark.django_db
def test_login_failure_invalid_credentials(create_user):
    """Test login failure with invalid credentials."""
    create_user(email="testuser@gmail.com", password="password123", is_email_verified=True,phone_number="1234567899")
    payload = {"username": "testuser@gmail.com", "password": "wrongpassword"}

    response = client.post("/user/login", payload)
    response_data = response.json()

    assert response.status_code == 401
    assert response_data["message"] == "Incorrect credentials."

@pytest.mark.django_db
def test_login_failure_unverified_email(create_user):
    """Test login failure with unverified email."""
    create_user(email="testuser@gmail.com", password="password123", is_email_verified=False,phone_number="1234567899")
    payload = {"username": "testuser@gmail.com", "password": "password123"}

    response = client.post("/user/login", payload)
    response_data = response.json()

    assert response.status_code == 403
    assert response_data["message"] == "Please verify your email to log in to your account."


# LOGOUT TESTS

@pytest.mark.django_db
def test_logout_success(create_user):
    """Test successful logout."""
    user = create_user(email="testuser@gmail.com", password="password123", is_email_verified=True,phone_number="1234567899")
    token = jwt.encode(
        {"id": user.anwesha_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
        COOKIE_ENCRYPTION_SECRET,
        algorithm="HS256"
    )

    client.cookies["jwt"] = token

    response = client.post("/user/logout")
    response_data = response.json()

    assert response_data['status'] == '200'
    assert response_data["message"] == "Logout Successful"

@pytest.mark.django_db
def test_logout_failure_no_token():
    """Test logout failure when no token is provided."""
    response = client.post("/user/logout")
    response_data = response.json()
    assert response.status_code == 401
    assert response_data["message"] == "Unauthenticated"


# EDIT PROFILE TESTS

@pytest.mark.django_db
def test_get_profile_success(create_user, generate_token):
    user = create_user(email="swayamsjain2242@gmail.com", password="password123", is_email_verified=True,phone_number="1234567809")
    client.cookies['jwt'] = generate_token(anwesha_id=user.anwesha_id)
    response = client.get("/user/editprofile")
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["anwesha_id"] == user.anwesha_id
    assert response_data["full_name"] == user.full_name
    assert response_data["email_id"] == user.email_id

@pytest.mark.django_db
def test_get_profile_unauthenticated():
    del client.cookies['jwt']
    response = client.get("/user/editprofile")
    assert response.status_code == 401
    assert response.json()["message"] == "You are unauthenticated. Please log in first."

@pytest.mark.django_db
def test_update_profile_success(create_user, generate_token):
    user = create_user(email="swayamsjain2242@gmail.com", password="password123", is_email_verified=True,phone_number="1234567809")
    client.cookies['jwt'] = generate_token(anwesha_id=user.anwesha_id)
    payload = {
        "full_name": "Updated Name",
        "college_name": "Updated College",
        "age": 26,
        "gender": "female",
        "instagram_id": "updated_insta",
        "facebook_id": "updated_fb",
    }

    response = client.post("/user/editprofile", data=payload)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["message"] == "Profile successfully updated!"

    # Verify the user is updated
    user.refresh_from_db()
    assert user.full_name == "Updated Name"
    assert user.collage_name == "Updated College"
    assert user.age == 26
    assert user.gender == User.Gender.FEMALE
    assert user.instagram_id == "updated_insta"
    assert user.facebook_id == "updated_fb"

@pytest.mark.django_db
def test_update_profile_unauthenticated():
    payload = {"full_name": "Unauthorized Update"}
    del client.cookies['jwt']
    response = client.post("/user/editprofile", data=payload)

    assert response.status_code == 401
    assert response.json()["message"] == "You are unauthenticated. Please log in first."


# VERIFY EMAIL TOKEN TESTS

@pytest.mark.django_db
def test_verify_email_success(create_user, generate_token):
    """Test successful email verification."""
    user = create_user(email="swayamsjain2242@gmail.com", password="password123", is_email_verified=False,phone_number="1234567809")
    token = generate_token(anwesha_id=user.anwesha_id)
    url = '/user/verifyemail/'+token
    response = client.get(url)

    assert response.status_code == 302  
    user.refresh_from_db()
    assert user.is_email_verified is True