from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL
DATABASE_URL = "sqlite:///./emailace.db"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Email Model
class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    subject = Column(String, index=True)
    body = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String, default="neutral")  # positive, negative, neutral
    priority = Column(String, default="normal")    # urgent, high, normal, low
    status = Column(String, default="pending")    # pending, resolved, archived
    draft_reply = Column(Text, nullable=True)
    is_urgent = Column(Boolean, default=False)
    summary = Column(Text, nullable=True)
    entities = Column(Text, nullable=True)  # JSON string of extracted entities

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



