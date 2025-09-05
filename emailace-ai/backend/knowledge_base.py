"""
Knowledge Base for EmailAce AI
Implements RAG (Retrieval-Augmented Generation) for context-aware responses
"""

import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class KnowledgeEntry:
    """Knowledge base entry"""
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    embedding: Optional[np.ndarray] = None

class KnowledgeBase:
    """Knowledge base for RAG implementation"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.embedding_model = None
        self.entries: List[KnowledgeEntry] = []
        self.embeddings: Optional[np.ndarray] = None
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Failed to load embedding model: {e}")
            self.embedding_model = None
    
    def add_entry(self, entry: KnowledgeEntry):
        """Add a knowledge entry"""
        if self.embedding_model:
            # Generate embedding
            entry.embedding = self.embedding_model.encode(entry.content)
        
        self.entries.append(entry)
        
        # Update embeddings matrix
        if self.embedding_model and entry.embedding is not None:
            if self.embeddings is None:
                self.embeddings = entry.embedding.reshape(1, -1)
            else:
                self.embeddings = np.vstack([self.embeddings, entry.embedding.reshape(1, -1)])
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant knowledge entries"""
        if not self.embedding_model or self.embeddings is None:
            # Fallback to simple text search
            return self._simple_search(query, top_k)
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)
        
        # Calculate similarities
        similarities = cosine_similarity(
            query_embedding.reshape(1, -1), 
            self.embeddings
        )[0]
        
        # Get top-k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Minimum similarity threshold
                entry = self.entries[idx]
                results.append({
                    "id": entry.id,
                    "title": entry.title,
                    "content": entry.content,
                    "category": entry.category,
                    "tags": entry.tags,
                    "similarity": float(similarities[idx])
                })
        
        return results
    
    def _simple_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Simple text-based search fallback"""
        query_lower = query.lower()
        results = []
        
        for entry in self.entries:
            score = 0
            content_lower = entry.content.lower()
            title_lower = entry.title.lower()
            
            # Check title matches
            if query_lower in title_lower:
                score += 2
            
            # Check content matches
            if query_lower in content_lower:
                score += 1
            
            # Check tag matches
            for tag in entry.tags:
                if query_lower in tag.lower():
                    score += 1.5
            
            if score > 0:
                results.append({
                    "id": entry.id,
                    "title": entry.title,
                    "content": entry.content,
                    "category": entry.category,
                    "tags": entry.tags,
                    "similarity": score / 4.5  # Normalize to 0-1
                })
        
        # Sort by score and return top-k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def get_context_for_query(self, query: str, max_context_length: int = 1000) -> str:
        """Get relevant context for a query"""
        results = self.search(query, top_k=3)
        
        if not results:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        current_length = 0
        
        for result in results:
            content = result["content"]
            if current_length + len(content) <= max_context_length:
                context_parts.append(f"**{result['title']}**\n{content}")
                current_length += len(content)
            else:
                # Truncate if needed
                remaining = max_context_length - current_length
                if remaining > 100:  # Only add if there's meaningful content left
                    context_parts.append(f"**{result['title']}**\n{content[:remaining]}...")
                break
        
        return "\n\n".join(context_parts)
    
    def load_from_file(self, file_path: str):
        """Load knowledge base from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data:
                entry = KnowledgeEntry(
                    id=item["id"],
                    title=item["title"],
                    content=item["content"],
                    category=item["category"],
                    tags=item["tags"]
                )
                self.add_entry(entry)
            
            print(f"Loaded {len(data)} knowledge entries from {file_path}")
            
        except Exception as e:
            print(f"Failed to load knowledge base: {e}")
    
    def save_to_file(self, file_path: str):
        """Save knowledge base to JSON file"""
        try:
            data = []
            for entry in self.entries:
                data.append({
                    "id": entry.id,
                    "title": entry.title,
                    "content": entry.content,
                    "category": entry.category,
                    "tags": entry.tags
                })
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved {len(data)} knowledge entries to {file_path}")
            
        except Exception as e:
            print(f"Failed to save knowledge base: {e}")

# Initialize default knowledge base
def create_default_knowledge_base() -> KnowledgeBase:
    """Create a default knowledge base with common support scenarios"""
    kb = KnowledgeBase()
    
    # Add default entries
    default_entries = [
        KnowledgeEntry(
            id="server_outage",
            title="Server Outage Response",
            content="When a customer reports a server outage, acknowledge the critical nature immediately. Provide status updates every 30 minutes. Escalate to infrastructure team. Offer alternative solutions if available. Schedule post-incident review.",
            category="technical_issues",
            tags=["server", "outage", "downtime", "critical", "infrastructure"]
        ),
        KnowledgeEntry(
            id="payment_issues",
            title="Payment Processing Problems",
            content="For payment-related issues, verify the customer's account status first. Check for failed transactions, billing cycles, and payment methods. Provide step-by-step troubleshooting. Escalate to billing team if needed. Offer alternative payment methods.",
            category="billing",
            tags=["payment", "billing", "transaction", "failed", "credit_card"]
        ),
        KnowledgeEntry(
            id="feature_requests",
            title="Feature Request Handling",
            content="For feature requests, thank the customer for their input. Explain the product roadmap process. Take detailed notes about the requested feature. Forward to product team. Provide timeline estimates if available. Keep customer updated on progress.",
            category="product",
            tags=["feature", "request", "enhancement", "roadmap", "product"]
        ),
        KnowledgeEntry(
            id="account_access",
            title="Account Access Issues",
            content="For account access problems, verify user identity through security questions. Check account status and permissions. Guide through password reset process. Check for account locks or suspensions. Escalate to security team if suspicious activity.",
            category="account",
            tags=["login", "password", "access", "account", "security"]
        ),
        KnowledgeEntry(
            id="refund_requests",
            title="Refund and Cancellation Policy",
            content="For refund requests, check the refund policy and eligibility. Verify purchase details and reason for refund. Process refunds within 5-7 business days. Provide confirmation and tracking information. Follow up to ensure customer satisfaction.",
            category="billing",
            tags=["refund", "cancellation", "money_back", "policy", "billing"]
        ),
        KnowledgeEntry(
            id="api_issues",
            title="API Integration Problems",
            content="For API-related issues, check API documentation and status page. Verify API keys and authentication. Test endpoints and check rate limits. Provide code examples and troubleshooting steps. Escalate to developer support if needed.",
            category="technical_issues",
            tags=["api", "integration", "developer", "endpoints", "authentication"]
        ),
        KnowledgeEntry(
            id="general_greeting",
            title="Professional Email Greeting",
            content="Always start with a professional greeting. Acknowledge the customer's concern. Show empathy and understanding. Provide clear, actionable solutions. End with a professional closing and contact information.",
            category="communication",
            tags=["greeting", "professional", "empathy", "communication", "tone"]
        )
    ]
    
    for entry in default_entries:
        kb.add_entry(entry)
    
    return kb

# Global knowledge base instance
knowledge_base = create_default_knowledge_base()



