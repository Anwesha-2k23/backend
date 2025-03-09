import pytest
from rest_framework.test import APIClient
from .models import Multicity_Events, Multicity_Participants
from .models import Multicity_Participants

client = APIClient()

@pytest.fixture
def create_event():
    """
    Create a test event.
    """
    return Multicity_Events.objects.create(
        event_id="ev01",
        event_name="Test Event",
        event_description="A test event",
        event_date="2025-01-10 15:00:00"
    )

@pytest.mark.django_db
def test_register_success(create_event):
    """
    Test successful registration for an event.
    """
    url = "/multicity/register"
    payload = {
        "event_id": "ev01",
        "organisation_type": 1,
        "solo_team": True,
        "leader_name": "John Doe",
        "leader_email": "johndoe@example.com",
        "leader_phone_no": "1234567890",
        "leader_organisation": "Test College"
    }
    response = client.post(url, payload)

    assert response.status_code == 200
    assert "registration ID" in response.json()

@pytest.mark.django_db
def test_register_invalid_email(create_event):
    """
    Test registration with an invalid email address.
    """
    url = "/multicity/register"
    payload = {
        "event_id": "ev01",
        "organisation_type": 1,
        "solo_team": True,
        "leader_name": "John Doe",
        "leader_email": "invalid_email",
        "leader_phone_no": "1234567890",
        "leader_organisation": "Test College"
    }
    response = client.post(url, payload, format="json")

    assert response.status_code == 409
    assert response.json()["message"] == "Please enter valid email address"

@pytest.mark.django_db
def test_register_duplicate_registration(create_event):
    """
    Test duplicate registration for the same event by the same leader.
    """
    
    Multicity_Participants.objects.create(
        event_id=create_event,
        organisation_type=Multicity_Participants.Organisation_Type.COLLEGE,
        solo_team=True,
        leader_name="John Doe",
        leader_email="johndoe@example.com",
        leader_phone_no="1234567890",
        leader_organisation="Test College"
    )
    url = "/multicity/register"
    payload = {
        "event_id": "ev01",
        "organisation_type": 1,
        "solo_team": True,
        "leader_name": "John Doe",
        "leader_email": "johndoe@example.com",
        "leader_phone_no": "1234567890",
        "leader_organisation": "Test College"
    }
    response = client.post(url, payload)
    
    assert response.status_code == 409
    assert response.json()["message"] == "You have already registered for this event"

@pytest.mark.django_db
def test_register_missing_data(create_event):
    """
    Test registration with missing required fields.
    """
    url = "/multicity/register"
    payload = {
        "event_id": create_event.event_id,
        "leader_name": "John Doe",
    }
    response = client.post(url, payload)

    assert response.status_code == 400
    assert response.json()["message"] == "Form data incomplete"
