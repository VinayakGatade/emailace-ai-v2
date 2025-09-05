#!/usr/bin/env python3
"""
Demo script for EmailAce AI
Tests the core functionality and displays results
"""

import sys
import os
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from ai_processor import AIProcessor
from knowledge_base import knowledge_base
from priority_queue import email_queue, Priority

def test_ai_processor():
    """Test AI processor functionality"""
    print("🤖 Testing AI Processor...")
    print("-" * 40)
    
    ai = AIProcessor()
    
    # Test emails
    test_emails = [
        {
            "subject": "URGENT: Server Down - Need Immediate Assistance",
            "body": "Hi team, our production server has been down for the past 2 hours. This is critical and affecting all our customers. We need immediate assistance to get this resolved. Please contact me at 555-123-4567 as soon as possible."
        },
        {
            "subject": "Thank you for the excellent service!",
            "body": "I just wanted to take a moment to express my gratitude for the outstanding service your team provided last week. The project was delivered on time and exceeded all our expectations."
        },
        {
            "subject": "API Integration Question",
            "body": "Hi, I'm having trouble integrating your API with our system. The authentication seems to be failing. Could you help me troubleshoot this? My email is developer@company.com"
        }
    ]
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n📧 Test Email {i}:")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body'][:100]}...")
        
        # Process email
        result = ai.process_email(email['body'], email['subject'])
        
        print(f"\n📊 AI Analysis:")
        print(f"  Sentiment: {result['sentiment']}")
        print(f"  Priority: {result['priority']}")
        print(f"  Urgent: {result['is_urgent']}")
        print(f"  Summary: {result['summary'][:100]}...")
        print(f"  Entities: {result['entities']}")
        print(f"  Draft Reply: {result['draft_reply'][:200]}...")

def test_knowledge_base():
    """Test knowledge base functionality"""
    print("\n\n🧠 Testing Knowledge Base...")
    print("-" * 40)
    
    queries = [
        "server outage",
        "payment issues",
        "feature request",
        "account login problems"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        results = knowledge_base.search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"  Result {i}: {result['title']} (similarity: {result['similarity']:.2f})")
            print(f"    Content: {result['content'][:100]}...")

def test_priority_queue():
    """Test priority queue functionality"""
    print("\n\n⚡ Testing Priority Queue...")
    print("-" * 40)
    
    # Clear existing queue
    email_queue.clear_processed()
    
    # Add test emails
    test_emails = [
        (1, "urgent", datetime.now()),
        (2, "normal", datetime.now()),
        (3, "high", datetime.now()),
        (4, "low", datetime.now()),
        (5, "urgent", datetime.now())
    ]
    
    for email_id, priority, created_at in test_emails:
        email_queue.add_email(email_id, priority, created_at)
        print(f"Added email {email_id} with priority {priority}")
    
    # Get queue status
    status = email_queue.get_queue_status()
    print(f"\n📊 Queue Status:")
    print(f"  Total pending: {status['total_pending']}")
    print(f"  Urgent: {status['urgent']}")
    print(f"  High: {status['high']}")
    print(f"  Normal: {status['normal']}")
    print(f"  Low: {status['low']}")
    
    # Process emails in priority order
    print(f"\n🔄 Processing emails in priority order:")
    while True:
        next_email = email_queue.get_next_email()
        if not next_email:
            break
        
        print(f"  Processing email {next_email.email_id} (priority: {next_email.priority.name})")
        email_queue.mark_processed(next_email.email_id)

def test_email_filtering():
    """Test email filtering functionality"""
    print("\n\n📧 Testing Email Filtering...")
    print("-" * 40)
    
    test_subjects = [
        "URGENT: Server Down - Need Immediate Assistance",
        "Thank you for the excellent service!",
        "API Integration Question",
        "Meeting Request for Next Week",
        "Support Request: Payment Issue",
        "Help with Account Access",
        "Query about Product Features"
    ]
    
    support_keywords = ["support", "query", "request", "help", "issue", "problem"]
    
    print("Filtering emails for support-related content:")
    for subject in test_subjects:
        is_support = any(keyword in subject.lower() for keyword in support_keywords)
        status = "✅ SUPPORT" if is_support else "❌ NOT SUPPORT"
        print(f"  {status}: {subject}")

def main():
    """Main demo function"""
    print("🚀 EmailAce AI Demo")
    print("=" * 50)
    print("This demo showcases the core functionality of EmailAce AI")
    print("=" * 50)
    
    try:
        # Test AI Processor
        test_ai_processor()
        
        # Test Knowledge Base
        test_knowledge_base()
        
        # Test Priority Queue
        test_priority_queue()
        
        # Test Email Filtering
        test_email_filtering()
        
        print("\n\n🎉 Demo completed successfully!")
        print("\nKey Features Demonstrated:")
        print("✅ AI-powered sentiment analysis and urgency detection")
        print("✅ RAG-enhanced response generation")
        print("✅ Priority queue for email processing")
        print("✅ Support email filtering")
        print("✅ Entity extraction and summarization")
        
        print("\n🚀 Next Steps:")
        print("1. Run 'python setup.py' to install dependencies")
        print("2. Configure email credentials in .env file")
        print("3. Start backend: cd backend && python run.py")
        print("4. Start frontend: npm run dev")
        print("5. Visit http://localhost:3000 to see the full application")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure you have installed the dependencies:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()



