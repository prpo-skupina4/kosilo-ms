import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import time, timedelta, date
from api import addTime


client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/kosilo/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_endpoint_invalid_data():
    """Test the create endpoint with invalid data"""
    response = client.post(
        "/kosilo/",
        json={
            "uporabnik_id": "invalid",  # should be int
            "dan": 3,
            "udelezenci": [1, 2, 3]
        }
    )
    assert response.status_code == 422  # Validation error


def test_create_endpoint_missing_fields():
    """Test the create endpoint with missing required fields"""
    response = client.post(
        "/kosilo/",
        json={
            "uporabnik_id": 1,
            # missing 'dan' and 'udelezenci'
        }
    )
    assert response.status_code == 422  # Validation error


def test_addTime_function():
    """Test the addTime utility function"""
    # Test adding 30 minutes to 12:00
    result = addTime(time(12, 0), timedelta(minutes=30))
    assert result == time(12, 30)
    
    # Test adding 1 hour to 10:00
    result = addTime(time(10, 0), timedelta(hours=1))
    assert result == time(11, 0)
    
    # Test adding time that crosses hour boundary
    result = addTime(time(10, 45), timedelta(minutes=30))
    assert result == time(11, 15)


def test_create_endpoint_success(httpx_mock):
    """Test the create endpoint with valid data and mocked external services"""
    from config import BOOL_URL, EV_URL
    
    # Mock the response from BOOL_URL (boolean service)
    httpx_mock.add_response(
        url=f"{BOOL_URL}/",
        method="POST",
        json=[
            {
                "dan": 1,
                "zacetek": "10:00:00",
                "dolzina": 60
            }
        ]
    )
    
    # Mock the response from EV_URL (event-view service)
    httpx_mock.add_response(
        url=f"{EV_URL}/urniki/1/termini",
        method="POST",
        json={
            "termin_id": 123,
            "zacetek": "09:00:00",
            "dolzina": 30,
            "dan": 3,
            "lokacija": "kosilo",
            "tip": "kosilo"
        },
        status_code=201
    )
    
    # Make the request with valid data
    response = client.post(
        "/kosilo/",
        headers={"Authorization": "Bearer test-token"},
        json={
            "uporabnik_id": 1,
            "dan": 3,
            "udelezenci": [1, 2, 3]
        }
    )
    
    # The endpoint should succeed (note: it returns None/204 on success based on the code)
    assert response.status_code in [200, 201, 204]


def test_create_endpoint_missing_authorization():
    """Test the create endpoint without Authorization header"""
    response = client.post(
        "/kosilo/",
        json={
            "uporabnik_id": 1,
            "dan": 3,
            "udelezenci": [1, 2, 3]
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing Authorization header"
