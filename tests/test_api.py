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
        "/kosilo/create",
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
        "/kosilo/create",
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
