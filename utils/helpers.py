import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import openai

# Import necessary packages
from fastapi import HTTPException
from dotenv import load_dotenv  
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

# Load environment variables from .env file
load_dotenv()

# API Key for OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OpenAI service for generating responses
openai_service = openai.OpenAI(api_key=OPENAI_API_KEY)

# Constants for caching
CACHE_TTL_SECONDS = 3600  # Cache validity in seconds
CACHE_MAX_SIZE = 1000  # Maximum number of cached responses

# Initialize the cache (using a simple dictionary for MVP)
CACHE = {}

def format_response(response: Dict[str, Any]) -> str:
    """
    Formats the response from the OpenAI API into a user-friendly format.
    """
    if isinstance(response, str):
        return response
    elif isinstance(response, dict) and "choices" in response:
        return response["choices"][0]["text"]
    else:
        return json.dumps(response, indent=2)

def log_request(request: schemas.RequestCreate, response: schemas.RequestResponse) -> None:
    """
    Logs request and response data for debugging and analysis.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Request: {request.text}")
    print(f"[{timestamp}] Response: {response.response}")

def validate_input(input_data: str) -> str:
    """
    Validates user input to ensure data integrity and prevent malicious attacks.
    """
    # Basic validation checks (add more as needed)
    if len(input_data) > 1000:
        raise HTTPException(status_code=400, detail="Input too long.")
    return input_data

def cache_response(response: schemas.RequestResponse) -> None:
    """
    Caches OpenAI responses to improve performance for frequently asked questions.
    """
    global CACHE
    # Use the request text as the key for caching
    cache_key = response.text
    # Add response to the cache, including the creation timestamp
    CACHE[cache_key] = (response, datetime.utcnow())
    # Remove old entries if cache size exceeds the maximum 
    if len(CACHE) > CACHE_MAX_SIZE:
        cleanup_cache()

def get_cached_response(request: schemas.RequestCreate) -> Optional[schemas.RequestResponse]:
    """
    Retrieves cached responses if available, optimizing performance.
    """
    global CACHE
    cache_key = request.text
    if cache_key in CACHE:
        response, cached_timestamp = CACHE[cache_key]
        # Check if the cached response is still valid based on the TTL
        if (datetime.utcnow() - cached_timestamp).total_seconds() <= CACHE_TTL_SECONDS:
            return response
    return None

def cleanup_cache() -> None:
    """
    Removes expired or unused cached data, managing cache size and efficiency.
    """
    global CACHE
    # Remove entries that have exceeded the TTL
    for cache_key, (response, cached_timestamp) in list(CACHE.items()):
        if (datetime.utcnow() - cached_timestamp).total_seconds() > CACHE_TTL_SECONDS:
            del CACHE[cache_key]

def generate_unique_id() -> str:
    """
    Generates a unique ID for each request, ensuring data integrity and tracking.
    """
    # Use a combination of timestamp and random string for ID generation 
    return f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{os.urandom(8).hex()}"

def format_timestamp(timestamp: datetime) -> str:
    """
    Formats timestamps into a consistent format for display and logging.
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")