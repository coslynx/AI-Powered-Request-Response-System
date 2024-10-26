from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    response = Column(String)
    created_at = Column(DateTime)