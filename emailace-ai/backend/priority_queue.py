"""
Priority Queue for Email Processing
Handles urgent email processing with proper prioritization
"""

import heapq
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Priority(Enum):
    """Email priority levels"""
    URGENT = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

@dataclass
class EmailTask:
    """Email processing task"""
    email_id: int
    priority: Priority
    created_at: datetime
    processed: bool = False
    retry_count: int = 0
    max_retries: int = 3
    
    def __lt__(self, other):
        """Comparison for heapq - lower priority number = higher priority"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        # If same priority, older emails first
        return self.created_at < other.created_at

class EmailPriorityQueue:
    """Priority queue for email processing"""
    
    def __init__(self):
        self.queue: List[EmailTask] = []
        self.processed_emails: set = set()
        self.failed_emails: set = set()
    
    def add_email(self, email_id: int, priority: str, created_at: datetime = None) -> bool:
        """Add email to priority queue"""
        if email_id in self.processed_emails or email_id in self.failed_emails:
            return False
        
        if created_at is None:
            created_at = datetime.now()
        
        # Convert string priority to enum
        priority_enum = self._parse_priority(priority)
        
        task = EmailTask(
            email_id=email_id,
            priority=priority_enum,
            created_at=created_at
        )
        
        heapq.heappush(self.queue, task)
        return True
    
    def get_next_email(self) -> Optional[EmailTask]:
        """Get next email to process (highest priority)"""
        while self.queue:
            task = heapq.heappop(self.queue)
            
            if task.email_id in self.processed_emails:
                continue  # Skip already processed emails
            
            return task
        
        return None
    
    def mark_processed(self, email_id: int) -> bool:
        """Mark email as successfully processed"""
        self.processed_emails.add(email_id)
        return True
    
    def mark_failed(self, email_id: int, retry: bool = True) -> bool:
        """Mark email as failed, optionally retry"""
        if retry:
            # Find the task and increment retry count
            for task in self.queue:
                if task.email_id == email_id:
                    task.retry_count += 1
                    if task.retry_count < task.max_retries:
                        # Re-add to queue with higher priority
                        task.priority = Priority.URGENT
                        heapq.heappush(self.queue, task)
                        return True
                    break
        
        self.failed_emails.add(email_id)
        return True
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        urgent_count = sum(1 for task in self.queue if task.priority == Priority.URGENT)
        high_count = sum(1 for task in self.queue if task.priority == Priority.HIGH)
        normal_count = sum(1 for task in self.queue if task.priority == Priority.NORMAL)
        low_count = sum(1 for task in self.queue if task.priority == Priority.LOW)
        
        return {
            "total_pending": len(self.queue),
            "urgent": urgent_count,
            "high": high_count,
            "normal": normal_count,
            "low": low_count,
            "processed": len(self.processed_emails),
            "failed": len(self.failed_emails)
        }
    
    def clear_processed(self):
        """Clear processed emails from memory"""
        self.processed_emails.clear()
        self.failed_emails.clear()
    
    def _parse_priority(self, priority: str) -> Priority:
        """Parse priority string to enum"""
        priority_lower = priority.lower()
        
        if priority_lower in ["urgent", "critical", "emergency"]:
            return Priority.URGENT
        elif priority_lower in ["high", "important"]:
            return Priority.HIGH
        elif priority_lower in ["normal", "medium", "standard"]:
            return Priority.NORMAL
        else:
            return Priority.LOW
    
    def get_urgent_emails(self) -> List[EmailTask]:
        """Get all urgent emails in the queue"""
        urgent_emails = []
        temp_queue = []
        
        # Extract urgent emails
        while self.queue:
            task = heapq.heappop(self.queue)
            if task.priority == Priority.URGENT:
                urgent_emails.append(task)
            else:
                temp_queue.append(task)
        
        # Restore non-urgent emails
        for task in temp_queue:
            heapq.heappush(self.queue, task)
        
        return urgent_emails

# Global priority queue instance
email_queue = EmailPriorityQueue()



