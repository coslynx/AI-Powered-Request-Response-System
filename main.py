from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import schemas
from routers import requests
from services.openai_service import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Database setup
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Register API routers
app.include_router(requests.router, prefix="/requests", tags=["requests"])

@app.on_event("startup")
async def startup_event():
    # Initialize the OpenAI service with API key from .env
    global openai_service
    openai_service = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connections and clean up resources
    pass