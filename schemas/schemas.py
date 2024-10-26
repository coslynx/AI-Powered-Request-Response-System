from pydantic import BaseModel, Field
from datetime import datetime

class RequestCreate(BaseModel):
    text: str = Field(..., description="Text of the request")

class RequestResponse(BaseModel):
    id: int 
    text: str
    response: str
    created_at: datetime