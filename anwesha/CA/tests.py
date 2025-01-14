import pytest
from CA.models import Campus_ambassador
from user.models import User
from utility import hashpassword
from rest_framework.test import APIClient

client = APIClient()

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
@pytest.mark.django_db
def test_ca():
    """
    Fixture for creating a test campus ambassador.
    """
    return Campus_ambassador.objects.create(
        email_id="test@example.com",
        password=hashpassword("testpass"),
        phone_number="1234567890",
        full_name="Test User",
        college_name="Test College",
        ca_id="CA12345",
        validation=True
    )

@pytest.fixture
@pytest.mark.django_db
def login_simulation(test_ca):
    url = "/campasambassador/login" 
    data = {
        "username": test_ca.email_id,
        "password": "testpass"
    }
    response = client.post(url, data)
    return client.cookies["jwt"]

@pytest.mark.django_db
def test_all_campas_ambassador(test_ca):
    url = "/campasambassador/allcampusambassadors"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email_id"] == "test@example.com"


@pytest.mark.django_db
def test_register_campus_ambassador():
    url = "/campasambassador/register"  
    data = {
        "email_id": "new_ca@example.com",
        "password": "newpassword",
        "phone_number": "1234567899",
        "full_name": "New CA",
        "college_name": "New College"
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["message"] == "Campus ambassador created successfully!"
    
@pytest.mark.django_db
def test_login_campus_ambassador(test_ca):
    url = "/campasambassador/login" 
    data = {
        "username": test_ca.email_id,
        "password": "testpass"
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.cookies["jwt"]
    assert response.data["success"] == True

@pytest.mark.django_db
def test_logout_campus_ambassador(test_ca,login_simulation):
    client.cookies["jwt"] = login_simulation
    url = "/campasambassador/logout"
    response = client.post(url)
    assert response.status_code == 200
    assert response.json()["message"] == "Logout Successful"

@pytest.mark.django_db
def test_edit_profile(test_ca,login_simulation):
    token = login_simulation 
    client.cookies["jwt"] = token

    url = "/campasambassador/editprofile"
    data = {
        "full_name": "Updated Name",
        "college_city": "Updated City"
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 200
    assert response.json()["message"] == "Profile successfully updated!"
    updated_ca = Campus_ambassador.objects.get(ca_id=test_ca.ca_id)
    assert updated_ca.full_name == "Updated Name"
    assert updated_ca.college_city == "Updated City"

@pytest.mark.django_db
def test_leaderboard_data(test_ca):
    test_ca.score = 100
    test_ca.save()

    url = "/campasambassador/leaderboarddata"
    response = client.get(url)
    assert response.status_code == 200
    leaderboard = response.json()["leaderBoardData"]
    assert len(leaderboard) == 1
    assert leaderboard[0]["score"] == 100
    assert leaderboard[0]["full_name"] == "Test User"
