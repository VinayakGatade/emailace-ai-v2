import re
import json
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List, Tuple
from knowledge_base import knowledge_base

class AIProcessor:
    def __init__(self):
        # Initialize NLP pipelines with safe fallbacks
        self.sentiment_analyzer = None
        self.summarizer = None

        try:
            # Correct public model id for SST-2 finetuned DistilBERT
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=True
            )
        except Exception as e:
            print(f"Sentiment pipeline load error: {e}")

        try:
            # T5-small summarizer
            self.summarizer = pipeline(
                "summarization",
                model="t5-small",
                max_length=100,
                min_length=30
            )
        except Exception as e:
            print(f"Summarization pipeline load error: {e}")
        
        # Urgency keywords
        self.urgency_keywords = [
            "urgent", "critical", "immediately", "asap", "emergency",
            "deadline", "important", "priority", "rush", "quick"
        ]
        
        # Entity patterns
        self.entity_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "url": r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        }
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of email text"""
        try:
            if self.sentiment_analyzer is None:
                # Simple heuristic fallback
                text_lower = text.lower()
                positive_words = ["great", "good", "awesome", "thanks", "thank you", "love", "happy"]
                negative_words = ["bad", "issue", "problem", "not working", "hate", "angry", "sad", "sorry"]
                pos_hits = sum(1 for w in positive_words if w in text_lower)
                neg_hits = sum(1 for w in negative_words if w in text_lower)
                if pos_hits > neg_hits:
                    return 'positive'
                if neg_hits > pos_hits:
                    return 'negative'
                return 'neutral'

            result = self.sentiment_analyzer(text[:512])  # Limit text length
            scores = result[0]

            # Find the highest scoring sentiment
            max_score = max(scores, key=lambda x: x['score'])

            if max_score['label'] == 'POSITIVE':
                return 'positive'
            elif max_score['label'] == 'NEGATIVE':
                return 'negative'
            else:
                return 'neutral'
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 'neutral'
    
    def detect_urgency(self, text: str) -> Tuple[str, bool]:
        """Detect urgency level and flag"""
        text_lower = text.lower()
        urgency_count = sum(1 for keyword in self.urgency_keywords if keyword in text_lower)
        
        if urgency_count >= 2:
            return "urgent", True
        elif urgency_count >= 1:
            return "high", True
        else:
            return "normal", False
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities using regex patterns"""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type] = list(set(matches))  # Remove duplicates
        
        return entities
    
    def generate_summary(self, text: str) -> str:
        """Generate summary of email text"""
        try:
            if len(text) < 100:
                return text
            
            # Limit text for summarization
            text_for_summary = text[:1000]
            if self.summarizer is None:
                # Fallback: return a truncated excerpt
                return text_for_summary[:200] + ("..." if len(text_for_summary) > 200 else "")

            summary = self.summarizer(text_for_summary, max_length=100, min_length=30)

            return summary[0]['summary_text']
        except Exception as e:
            print(f"Summarization error: {e}")
            return text[:200] + "..." if len(text) > 200 else text
    
    def generate_draft_reply(self, email_subject: str, email_body: str, sentiment: str) -> str:
        """Generate a context-aware draft reply using RAG"""
        # Get relevant context from knowledge base
        query = f"{email_subject} {email_body}"
        context = knowledge_base.get_context_for_query(query, max_context_length=800)
        
        # Base templates with RAG-enhanced responses
        templates = {
            "positive": [
                "Thank you for your positive feedback! I'm glad we could help.",
                "I appreciate your kind words. It's great to hear that everything is working well.",
                "Thank you for the positive review. We're committed to maintaining this level of service."
            ],
            "negative": [
                "I understand your concerns and I apologize for any inconvenience caused.",
                "Thank you for bringing this to our attention. We take feedback seriously and will address this promptly.",
                "I'm sorry to hear about your experience. Let me help resolve this issue for you."
            ],
            "neutral": [
                "Thank you for reaching out. I'll be happy to assist you with your request.",
                "I've received your message and will get back to you with the information you need.",
                "Thank you for contacting us. I'm here to help with your inquiry."
            ]
        }
        
        # Select base template
        template = templates.get(sentiment, templates["neutral"])
        import random
        base_reply = random.choice(template)
        
        # Enhance with context-aware information
        enhanced_reply = self._enhance_with_context(base_reply, context, email_subject, email_body, sentiment)
        
        return enhanced_reply
    
    def _enhance_with_context(self, base_reply: str, context: str, subject: str, body: str, sentiment: str) -> str:
        """Enhance reply with context from knowledge base"""
        # Check for specific issue types and provide relevant guidance
        issue_indicators = {
            "server": ["server", "down", "outage", "downtime", "not working"],
            "payment": ["payment", "billing", "charge", "refund", "money"],
            "account": ["login", "password", "access", "account", "sign in"],
            "api": ["api", "integration", "endpoint", "developer", "code"],
            "feature": ["feature", "request", "enhancement", "improvement", "suggestion"]
        }
        
        detected_issues = []
        body_lower = body.lower()
        subject_lower = subject.lower()
        
        for issue_type, keywords in issue_indicators.items():
            if any(keyword in body_lower or keyword in subject_lower for keyword in keywords):
                detected_issues.append(issue_type)
        
        # Build enhanced response
        enhanced_reply = base_reply
        
        if detected_issues:
            enhanced_reply += "\n\nBased on your message, I can see this relates to:"
            for issue in detected_issues:
                enhanced_reply += f"\n• {issue.replace('_', ' ').title()}"
        
        # Add context-specific guidance
        if context and "No relevant information found" not in context:
            enhanced_reply += f"\n\nHere's what I can help you with:\n{context[:500]}..."
        
        # Add urgency handling
        if "urgent" in subject_lower or "urgent" in body_lower or "critical" in body_lower:
            enhanced_reply += "\n\nI'm prioritizing this issue and will provide updates every 30 minutes until resolved."
        
        # Add next steps
        if sentiment == "negative":
            enhanced_reply += "\n\nI'll personally follow up on this to ensure we resolve it to your satisfaction."
        elif "?" in body or "question" in subject_lower:
            enhanced_reply += "\n\nI'll research this thoroughly and provide you with a detailed response within 24 hours."
        
        # Professional closing
        enhanced_reply += "\n\nBest regards,\nSupport Team"
        
        return enhanced_reply
    
    def process_email(self, email_text: str, email_subject: str = "") -> Dict:
        """Process email with all AI features"""
        # Analyze sentiment
        sentiment = self.analyze_sentiment(email_text)
        
        # Detect urgency
        priority, is_urgent = self.detect_urgency(email_text + " " + email_subject)
        
        # Extract entities
        entities = self.extract_entities(email_text)
        
        # Generate summary
        summary = self.generate_summary(email_text)
        
        # Generate draft reply
        draft_reply = self.generate_draft_reply(email_subject, email_text, sentiment)
        
        return {
            "sentiment": sentiment,
            "priority": priority,
            "is_urgent": is_urgent,
            "entities": entities,
            "summary": summary,
            "draft_reply": draft_reply
        }


