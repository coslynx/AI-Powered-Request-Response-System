import pytest
from sqlalchemy.orm import Session
from datetime import datetime
from unittest.mock import patch  # Import for mocking OpenAI responses

import models
import schemas
from database import get_db, engine  # Import database functions for testing
from services.openai_service import openai_service  # Import OpenAI service for mocking responses

# Create all tables in the database (run once for the entire test suite)
models.Base.metadata.create_all(bind=engine)

# Define fixture for creating a database session for each test function
@pytest.fixture(scope="function")
def db():
    """
    Creates a database session for each test function, ensuring a clean state for each test.

    Yields:
        Session: A database session for testing.

    """
    db = get_db()
    try:
        yield db
    finally:
        db.close()

# Define test function for verifying the Request model definition
def test_request_model(db: Session):
    """
    Tests the definition of the `Request` model, ensuring it has the expected attributes, data types, and relationships.

    Args:
        db (Session): A database session for testing.

    """
    assert hasattr(models.Request, "id")
    assert models.Request.id.primary_key is True
    assert models.Request.id.type is int
    assert hasattr(models.Request, "text")
    assert models.Request.text.type is str
    assert hasattr(models.Request, "response")
    assert models.Request.response.type is str
    assert hasattr(models.Request, "created_at")
    assert models.Request.created_at.type is datetime

# Define test function for creating a new Request record
def test_create_request(db: Session):
    """
    Tests creating a new `Request` record in the database, verifying the record is inserted correctly.

    Args:
        db (Session): A database session for testing.

    """
    test_request_data = schemas.RequestCreate(text="Test request")
    new_request = models.Request(**test_request_data.dict(), created_at=datetime.utcnow())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    assert new_request.text == test_request_data.text
    assert new_request.response is None  # Initially, response is None
    assert new_request.created_at is not None

# Define test function for reading an existing Request record
def test_read_request(db: Session):
    """
    Tests retrieving an existing `Request` record from the database, verifying the retrieved data is correct.

    Args:
        db (Session): A database session for testing.

    """
    test_request_data = schemas.RequestCreate(text="Test request")
    new_request = models.Request(**test_request_data.dict(), created_at=datetime.utcnow())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    fetched_request = db.query(models.Request).filter(models.Request.id == new_request.id).first()

    assert fetched_request is not None
    assert fetched_request.text == test_request_data.text
    assert fetched_request.response is None  # Initially, response is None
    assert fetched_request.created_at == new_request.created_at

# Define test function for updating an existing Request record
def test_update_request(db: Session):
    """
    Tests updating an existing `Request` record in the database, verifying the updated data is correct.

    Args:
        db (Session): A database session for testing.

    """
    test_request_data = schemas.RequestCreate(text="Test request")
    new_request = models.Request(**test_request_data.dict(), created_at=datetime.utcnow())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    # Mock OpenAI response for testing
    mock_response = "This is a mock response"

    # Patch the OpenAI service's generate_response method with a mock function
    with patch.object(openai_service, "generate_response", return_value=mock_response):
        new_request.response = mock_response
        db.commit()
        db.refresh(new_request)

        assert new_request.response == mock_response

# Define test function for deleting an existing Request record
def test_delete_request(db: Session):
    """
    Tests deleting an existing `Request` record from the database, verifying the record is removed.

    Args:
        db (Session): A database session for testing.

    """
    test_request_data = schemas.RequestCreate(text="Test request")
    new_request = models.Request(**test_request_data.dict(), created_at=datetime.utcnow())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    db.delete(new_request)
    db.commit()

    fetched_request = db.query(models.Request).filter(models.Request.id == new_request.id).first()
    assert fetched_request is None