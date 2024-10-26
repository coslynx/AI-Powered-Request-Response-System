"""
This file contains unit tests for the `main.py` file, ensuring the core application logic functions correctly.
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db  # Import the get_db function for database access in tests
from models import Request  # Import the Request model for testing database interactions
import schemas  # Import schemas to ensure data validation in tests
from services.openai_service import openai_service  # Import the OpenAI service for testing API calls
from unittest.mock import patch  # Import patch for mocking functions
from datetime import datetime

# Initialize the test client
client = TestClient(app)

# Define a test function for the root endpoint
def test_root():
    """
    Tests the root endpoint (/) of the FastAPI app.
    """
    response = client.get("/")
    assert response.status_code == 200

# Define a test function for creating a new request
@pytest.mark.asyncio
async def test_create_request():
    """
    Tests the POST /requests endpoint for creating a new request.
    """
    # Create a test request object using the Pydantic schema
    test_request = schemas.RequestCreate(text="Hello, world!")

    # Send the request to the API endpoint
    response = client.post("/requests", json=test_request.dict())

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response content type is JSON
    assert response.headers["Content-Type"] == "application/json"

    # Deserialize the response data as a RequestResponse object
    response_data = schemas.RequestResponse(**response.json())

    # Assert that the response data matches the expected values
    assert response_data.text == test_request.text
    assert response_data.response is not None

    # Check if the request is saved in the database
    with get_db() as db:
        db_request = db.query(Request).filter(Request.text == test_request.text).first()
        assert db_request is not None
        assert db_request.response is not None

# Define a test function for getting a specific request
@pytest.mark.asyncio
async def test_get_request():
    """
    Tests the GET /requests/{request_id} endpoint for retrieving a specific request.
    """
    # Create a test request using the OpenAI service
    test_request = schemas.RequestCreate(text="How are you?")
    test_response = await openai_service.generate_response(test_request.text)

    # Save the test request to the database
    with get_db() as db:
        new_request = models.Request(text=test_request.text, response=test_response, created_at=datetime.utcnow())
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        request_id = new_request.id

    # Send the request to the API endpoint
    response = client.get(f"/requests/{request_id}")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response content type is JSON
    assert response.headers["Content-Type"] == "application/json"

    # Deserialize the response data as a RequestResponse object
    response_data = schemas.RequestResponse(**response.json())

    # Assert that the response data matches the expected values
    assert response_data.id == request_id
    assert response_data.text == test_request.text
    assert response_data.response == test_response

# Define a test function for handling an OpenAI API error
@pytest.mark.asyncio
async def test_openai_api_error():
    """
    Tests the create_request endpoint when an OpenAI API error occurs.
    """
    # Mock the OpenAI service to raise an OpenAIError
    async def mock_generate_response(*args, **kwargs):
        raise openai.error.OpenAIError("Test OpenAI API error")

    # Patch the OpenAI service's generate_response method with the mock function
    with patch.object(openai_service, "generate_response", mock_generate_response):
        # Create a test request
        test_request = schemas.RequestCreate(text="This will cause an OpenAI error")

        # Send the request to the API endpoint
        response = client.post("/requests", json=test_request.dict())

        # Assert that the response status code is 500 (Internal Server Error)
        assert response.status_code == 500

        # Assert that the error message is in the response body
        assert "OpenAI API request failed: Test OpenAI API error" in response.text