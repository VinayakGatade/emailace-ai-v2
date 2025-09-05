from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class EmailBase(BaseModel):
    sender: str
    subject: str
    body: str

class EmailCreate(EmailBase):
    pass

class EmailResponse(EmailBase):
    id: int
    date: datetime
    sentiment: str
    priority: str
    status: str
    draft_reply: Optional[str] = None
    is_urgent: bool
    summary: Optional[str] = None
    entities: Optional[str] = None

    class Config:
        from_attributes = True

class EmailDetail(EmailResponse):
    pass

class ReplyRequest(BaseModel):
    custom_prompt: Optional[str] = None

class ReplyResponse(BaseModel):
    draft_reply: str
    sentiment: str
    priority: str
    summary: str
    entities: Dict[str, Any]

class AnalyticsResponse(BaseModel):
    total_emails: int
    resolved_emails: int
    pending_emails: int
    urgent_emails: int
    sentiment_breakdown: Dict[str, int]
    priority_breakdown: Dict[str, int]

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database_connected: bool


