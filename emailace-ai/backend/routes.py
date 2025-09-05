from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime
import os

from database import get_db, Email
from models import EmailResponse, EmailDetail, ReplyRequest, ReplyResponse, AnalyticsResponse, HealthResponse
from ai_processor import AIProcessor
from email_service import get_email_service
from priority_queue import email_queue

router = APIRouter()
ai_processor = AIProcessor()

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="Backend running 🚀",
        timestamp=datetime.utcnow(),
        database_connected=True
    )

@router.get("/emails", response_model=List[EmailResponse])
async def get_emails(db: Session = Depends(get_db)):
    """Get all emails with metadata, ordered by priority"""
    # Get emails ordered by priority (urgent first, then by date)
    emails = db.query(Email).order_by(
        Email.is_urgent.desc(),
        Email.priority.asc(),
        Email.date.desc()
    ).all()
    
    # Add emails to priority queue if not already processed
    for email in emails:
        if email.status == "pending":
            email_queue.add_email(
                email_id=email.id,
                priority=email.priority,
                created_at=email.date
            )
    
    return emails

@router.get("/emails/{email_id}", response_model=EmailDetail)
async def get_email_detail(email_id: int, db: Session = Depends(get_db)):
    """Get details of a single email"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    return email

@router.post("/emails/{email_id}/generate-reply", response_model=ReplyResponse)
async def generate_reply(
    email_id: int, 
    request: ReplyRequest, 
    db: Session = Depends(get_db)
):
    """Generate AI-powered reply for an email"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    # Process email with AI
    ai_results = ai_processor.process_email(email.body, email.subject)
    
    # Update email with new AI analysis
    email.sentiment = ai_results["sentiment"]
    email.priority = ai_results["priority"]
    email.is_urgent = ai_results["is_urgent"]
    email.summary = ai_results["summary"]
    email.entities = json.dumps(ai_results["entities"])
    email.draft_reply = ai_results["draft_reply"]
    
    # Commit changes
    db.commit()
    db.refresh(email)
    
    return ReplyResponse(
        draft_reply=ai_results["draft_reply"],
        sentiment=ai_results["sentiment"],
        priority=ai_results["priority"],
        summary=ai_results["summary"],
        entities=ai_results["entities"]
    )

@router.post("/emails/{email_id}/send-reply")
async def send_reply(email_id: int, db: Session = Depends(get_db)):
    """Mark email as resolved (simulate sending reply)"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    email.status = "resolved"
    db.commit()
    
    return {"message": "Email marked as resolved successfully"}

@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(db: Session = Depends(get_db)):
    """Get email analytics and statistics"""
    # Get total counts
    total_emails = db.query(Email).count()
    resolved_emails = db.query(Email).filter(Email.status == "resolved").count()
    pending_emails = db.query(Email).filter(Email.status == "pending").count()
    urgent_emails = db.query(Email).filter(Email.is_urgent == True).count()
    
    # Get sentiment breakdown
    sentiment_counts = {}
    for sentiment in ["positive", "negative", "neutral"]:
        count = db.query(Email).filter(Email.sentiment == sentiment).count()
        sentiment_counts[sentiment] = count
    
    # Get priority breakdown
    priority_counts = {}
    for priority in ["urgent", "high", "normal", "low"]:
        count = db.query(Email).filter(Email.priority == priority).count()
        priority_counts[priority] = count
    
    return AnalyticsResponse(
        total_emails=total_emails,
        resolved_emails=resolved_emails,
        pending_emails=pending_emails,
        urgent_emails=urgent_emails,
        sentiment_breakdown=sentiment_counts,
        priority_breakdown=priority_counts
    )

@router.post("/emails/{email_id}/archive")
async def archive_email(email_id: int, db: Session = Depends(get_db)):
    """Archive an email"""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )
    
    email.status = "archived"
    db.commit()
    
    return {"message": "Email archived successfully"}

@router.get("/emails/search/{query}")
async def search_emails(query: str, db: Session = Depends(get_db)):
    """Search emails by sender, subject, or body content"""
    search_results = db.query(Email).filter(
        (Email.sender.contains(query)) |
        (Email.subject.contains(query)) |
        (Email.body.contains(query))
    ).all()
    
    return search_results

@router.post("/emails/sync")
async def sync_emails(db: Session = Depends(get_db)):
    """Sync emails from external email provider"""
    try:
        # Get email service (default to Gmail)
        email_service = get_email_service("gmail")
        
        # Fetch emails from external provider
        external_emails = email_service.fetch_emails(since_days=7, limit=20)
        
        synced_count = 0
        for email_data in external_emails:
            # Check if email already exists
            existing_email = db.query(Email).filter(
                Email.sender == email_data['sender'],
                Email.subject == email_data['subject'],
                Email.date == email_data['date']
            ).first()
            
            if not existing_email:
                # Process with AI
                ai_results = ai_processor.process_email(
                    email_data['body'], 
                    email_data['subject']
                )
                
                # Create new email record
                new_email = Email(
                    sender=email_data['sender'],
                    subject=email_data['subject'],
                    body=email_data['body'],
                    date=datetime.fromisoformat(email_data['date'].replace('Z', '+00:00')),
                    sentiment=ai_results["sentiment"],
                    priority=ai_results["priority"],
                    status="pending",
                    is_urgent=ai_results["is_urgent"],
                    summary=ai_results["summary"],
                    entities=json.dumps(ai_results["entities"]),
                    draft_reply=ai_results["draft_reply"]
                )
                
                db.add(new_email)
                synced_count += 1
        
        db.commit()
        email_service.disconnect()
        
        return {
            "message": f"Successfully synced {synced_count} new emails",
            "synced_count": synced_count
        }
        
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Email sync failed: {str(e)}"
        )

@router.post("/emails/{email_id}/send-email")
async def send_email_reply(
    email_id: int, 
    reply_content: str,
    db: Session = Depends(get_db)
):
    """Send actual email reply"""
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email not found"
            )
        
        # Get email service
        email_service = get_email_service("gmail")
        
        # Send email
        success = email_service.send_email(
            to_email=email.sender,
            subject=f"Re: {email.subject}",
            body=reply_content,
            reply_to=os.getenv("REPLY_EMAIL", email.sender)
        )
        
        email_service.disconnect()
        
        if success:
            # Mark as resolved
            email.status = "resolved"
            db.commit()
            
            return {"message": "Email sent successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Email send failed: {str(e)}"
        )

@router.get("/queue/status")
async def get_queue_status():
    """Get priority queue status"""
    return email_queue.get_queue_status()

@router.get("/queue/next")
async def get_next_email():
    """Get next email to process from priority queue"""
    next_task = email_queue.get_next_email()
    if next_task:
        return {
            "email_id": next_task.email_id,
            "priority": next_task.priority.name,
            "created_at": next_task.created_at.isoformat(),
            "retry_count": next_task.retry_count
        }
    return {"message": "No emails in queue"}

@router.post("/queue/process/{email_id}")
async def process_email_from_queue(email_id: int, db: Session = Depends(get_db)):
    """Process an email from the queue"""
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            return {"error": "Email not found"}
        
        # Generate AI response
        ai_results = ai_processor.process_email(email.body, email.subject)
        
        # Update email with AI analysis
        email.sentiment = ai_results["sentiment"]
        email.priority = ai_results["priority"]
        email.is_urgent = ai_results["is_urgent"]
        email.summary = ai_results["summary"]
        email.entities = json.dumps(ai_results["entities"])
        email.draft_reply = ai_results["draft_reply"]
        
        db.commit()
        
        # Mark as processed in queue
        email_queue.mark_processed(email_id)
        
        return {
            "message": "Email processed successfully",
            "ai_results": ai_results
        }
        
    except Exception as e:
        email_queue.mark_failed(email_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Email processing failed: {str(e)}"
        )


