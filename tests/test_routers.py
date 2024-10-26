import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import patch, MagicMock

# Import necessary packages for testing.
import models
import schemas
from database import get_db, engine
from routers import requests
from services.openai_service import openai_service

# Create all tables in the database for test setup.
models.Base.metadata.create_all(bind=engine)

# Initialize the test client.
client = TestClient(requests.router)

# Define a test function for creating a new request.
@pytest.mark.asyncio
async def test_create_request():
    """
    Tests the POST /requests endpoint for creating a new request.
    """
    test_request_data = schemas.RequestCreate(text="Test request")

    # Mock the OpenAI service's generate_response method.
    mock_openai_response = "This is a mock OpenAI response"
    with patch.object(openai_service, "generate_response", return_value=mock_openai_response):
        # Send the request to the API endpoint.
        response = client.post("/", json=test_request_data.dict())

    # Assert the response status code and content type.
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Deserialize the response data as a RequestResponse object.
    response_data = schemas.RequestResponse(**response.json())

    # Assert that the response data matches the expected values.
    assert response_data.text == test_request_data.text
    assert response_data.response == mock_openai_response

    # Check if the request is saved in the database.
    with get_db() as db:
        db_request = db.query(models.Request).filter(models.Request.text == test_request_data.text).first()
        assert db_request is not None
        assert db_request.response == mock_openai_response

# Define a test function for getting a specific request.
@pytest.mark.asyncio
async def test_get_request():
    """
    Tests the GET /requests/{request_id} endpoint for retrieving a specific request.
    """
    test_request_data = schemas.RequestCreate(text="Test request")
    mock_openai_response = "This is a mock OpenAI response"

    # Create a test request and save it to the database.
    with get_db() as db:
        with patch.object(openai_service, "generate_response", return_value=mock_openai_response):
            new_request = models.Request(text=test_request_data.text, response=mock_openai_response, created_at=datetime.utcnow())
            db.add(new_request)
            db.commit()
            db.refresh(new_request)
            request_id = new_request.id

    # Send the request to the API endpoint.
    response = client.get(f"/{request_id}")

    # Assert the response status code and content type.
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Deserialize the response data as a RequestResponse object.
    response_data = schemas.RequestResponse(**response.json())

    # Assert that the response data matches the expected values.
    assert response_data.id == request_id
    assert response_data.text == test_request_data.text
    assert response_data.response == mock_openai_response

# Define a test function for handling an OpenAI API error.
@pytest.mark.asyncio
async def test_openai_api_error():
    """
    Tests the create_request endpoint when an OpenAI API error occurs.
    """
    test_request_data = schemas.RequestCreate(text="This will cause an OpenAI error")

    # Mock the OpenAI service to raise an OpenAIError.
    with patch.object(openai_service, "generate_response", side_effect=openai.error.OpenAIError("Test OpenAI API error")):
        # Send the request to the API endpoint.
        response = client.post("/", json=test_request_data.dict())

    # Assert that the response status code is 500 (Internal Server Error).
    assert response.status_code == 500

    # Assert that the error message is in the response body.
    assert "OpenAI API request failed: Test OpenAI API error" in response.text

# Define a test function for handling a general exception during request processing.
@pytest.mark.asyncio
async def test_general_exception():
    """
    Tests the create_request endpoint when a general exception occurs during request processing.
    """
    test_request_data = schemas.RequestCreate(text="This will cause a general exception")

    # Mock the OpenAI service to raise a general exception.
    with patch.object(openai_service, "generate_response", side_effect=Exception("Test general exception")):
        # Send the request to the API endpoint.
        response = client.post("/", json=test_request_data.dict())

    # Assert that the response status code is 500 (Internal Server Error).
    assert response.status_code == 500

    # Assert that the error message is in the response body.
    assert "Internal server error: Test general exception" in response.text

# Define a test function for handling a database error.
@pytest.mark.asyncio
async def test_database_error():
    """
    Tests the create_request endpoint when a database error occurs.
    """
    test_request_data = schemas.RequestCreate(text="This will cause a database error")

    # Mock the database session to raise an exception.
    with patch.object(Session, "add", side_effect=Exception("Test database error")):
        # Send the request to the API endpoint.
        response = client.post("/", json=test_request_data.dict())

    # Assert that the response status code is 500 (Internal Server Error).
    assert response.status_code == 500

    # Assert that the error message is in the response body.
    assert "Internal server error: Test database error" in response.text

# Define a test function for handling a request not found error.
@pytest.mark.asyncio
async def test_request_not_found():
    """
    Tests the GET /requests/{request_id} endpoint when the request is not found.
    """
    invalid_request_id = 999

    # Send the request to the API endpoint.
    response = client.get(f"/{invalid_request_id}")

    # Assert that the response status code is 404 (Not Found).
    assert response.status_code == 404

    # Assert that the error message is in the response body.
    assert "Request not found" in response.text