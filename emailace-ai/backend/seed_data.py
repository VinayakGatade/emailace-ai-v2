from datetime import datetime, timedelta
from database import Email, SessionLocal
from ai_processor import AIProcessor
import json

def seed_database():
    """Seed the database with sample emails"""
    db = SessionLocal()
    
    # Check if emails already exist
    existing_emails = db.query(Email).count()
    if existing_emails > 0:
        print("Database already seeded. Skipping...")
        db.close()
        return
    
    # Initialize AI processor
    ai_processor = AIProcessor()
    
    # Sample emails data
    sample_emails = [
        {
            "sender": "john.doe@company.com",
            "subject": "URGENT: Server Down - Need Immediate Assistance",
            "body": "Hi team, our production server has been down for the past 2 hours. This is critical and affecting all our customers. We need immediate assistance to get this resolved. Please contact me at 555-123-4567 as soon as possible. This is a top priority issue that needs to be addressed immediately.",
            "date": datetime.utcnow() - timedelta(hours=1)
        },
        {
            "sender": "sarah.wilson@client.com",
            "subject": "Thank you for the excellent service!",
            "body": "I just wanted to take a moment to express my gratitude for the outstanding service your team provided last week. The project was delivered on time and exceeded all our expectations. The attention to detail and professional approach really made a difference. I'll definitely recommend your company to others in the industry.",
            "date": datetime.utcnow() - timedelta(hours=3)
        },
        {
            "sender": "tech.support@vendor.com",
            "subject": "Software Update Available - Action Required",
            "body": "A new security update is available for your software. This update addresses critical vulnerabilities and should be installed within the next 48 hours. Please visit https://update.vendor.com to download and install the latest version. If you have any questions, contact our support team.",
            "date": datetime.utcnow() - timedelta(hours=5)
        },
        {
            "sender": "mike.johnson@partner.com",
            "subject": "Meeting Request for Next Week",
            "body": "Hi there, I'd like to schedule a meeting to discuss our upcoming collaboration project. I'm available on Tuesday and Thursday between 2-4 PM. Please let me know what works best for you. We can discuss the timeline, deliverables, and any questions you might have about the partnership.",
            "date": datetime.utcnow() - timedelta(hours=8)
        },
        {
            "sender": "complaints@customer.com",
            "subject": "Dissatisfied with Product Quality",
            "body": "I'm very disappointed with the quality of the product I received. It doesn't match the description on your website and arrived damaged. I've been a customer for 3 years and this is the first time I've had such a poor experience. I expect a full refund and compensation for the inconvenience caused.",
            "date": datetime.utcnow() - timedelta(hours=12)
        },
        {
            "sender": "hr@company.com",
            "subject": "Important: New Policy Implementation",
            "body": "Please be advised that we will be implementing new workplace policies starting next month. These changes affect remote work arrangements, vacation policies, and health benefits. All employees must review the new handbook by Friday. If you have questions, please contact HR at hr@company.com or call 555-987-6543.",
            "date": datetime.utcnow() - timedelta(hours=16)
        },
        {
            "sender": "sales@competitor.com",
            "subject": "Special Offer - Limited Time Only",
            "body": "We're offering an exclusive 30% discount on all our premium services for the next 7 days only! This is a fantastic opportunity to upgrade your current package and save money. Visit our website at https://competitor.com/offer or call us at 555-456-7890 to learn more about this limited-time promotion.",
            "date": datetime.utcnow() - timedelta(hours=20)
        },
        {
            "sender": "project.manager@team.com",
            "subject": "Weekly Status Update Required",
            "body": "Please submit your weekly status reports by end of day today. Include progress on current tasks, any blockers you're facing, and plans for next week. This information is needed for our client presentation tomorrow morning. If you have any issues or questions, please reach out to me directly.",
            "date": datetime.utcnow() - timedelta(hours=24)
        },
        {
            "sender": "feedback@service.com",
            "subject": "How was your experience today?",
            "body": "We hope you had a great experience using our service today! We'd love to hear your feedback. Your opinion helps us improve and provide better service to all our customers. Please take a moment to rate your experience and share any comments you might have. Thank you for choosing us!",
            "date": datetime.utcnow() - timedelta(hours=28)
        },
        {
            "sender": "admin@system.com",
            "subject": "System Maintenance Notice",
            "body": "Scheduled system maintenance will occur this Saturday from 2-6 AM EST. During this time, some services may be temporarily unavailable. We apologize for any inconvenience this may cause. All systems should be fully operational by 6 AM EST. If you experience any issues after maintenance, please contact our support team.",
            "date": datetime.utcnow() - timedelta(hours=32)
        }
    ]
    
    # Process and insert emails
    for email_data in sample_emails:
        # Process with AI
        ai_results = ai_processor.process_email(email_data["body"], email_data["subject"])
        
        # Create email object
        email = Email(
            sender=email_data["sender"],
            subject=email_data["subject"],
            body=email_data["body"],
            date=email_data["date"],
            sentiment=ai_results["sentiment"],
            priority=ai_results["priority"],
            status="pending",
            is_urgent=ai_results["is_urgent"],
            summary=ai_results["summary"],
            entities=json.dumps(ai_results["entities"]),
            draft_reply=ai_results["draft_reply"]
        )
        
        db.add(email)
    
    # Commit changes
    db.commit()
    db.close()
    
    print("Database seeded successfully with 10 sample emails!")

if __name__ == "__main__":
    seed_database()


