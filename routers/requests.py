from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

import models, schemas
from database import get_db
from services.openai_service import openai_service

router = APIRouter()

@router.post("/", response_model=schemas.RequestResponse)
async def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    try:
        response = await openai_service.generate_response(request.text)
        new_request = models.Request(text=request.text, response=response, created_at=datetime.utcnow())
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return new_request
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API request failed: {e}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.get("/{request_id}", response_model=schemas.RequestResponse)
async def get_request(request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request