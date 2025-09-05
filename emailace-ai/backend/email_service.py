"""
Email Service for EmailAce AI
Handles email retrieval from various providers (Gmail, IMAP, Outlook)
"""

import imaplib
import email
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dataclasses import dataclass

@dataclass
class EmailConfig:
    """Email configuration for different providers"""
    provider: str
    imap_server: str
    imap_port: int
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    use_ssl: bool = True

class EmailService:
    """Service for handling email operations"""
    
    def __init__(self, config: EmailConfig):
        self.config = config
        self.imap_connection = None
        self.smtp_connection = None
    
    def connect_imap(self) -> bool:
        """Connect to IMAP server"""
        try:
            if self.config.use_ssl:
                self.imap_connection = imaplib.IMAP4_SSL(
                    self.config.imap_server, 
                    self.config.imap_port
                )
            else:
                self.imap_connection = imaplib.IMAP4(
                    self.config.imap_server, 
                    self.config.imap_port
                )
            
            self.imap_connection.login(
                self.config.username, 
                self.config.password
            )
            return True
        except Exception as e:
            print(f"IMAP connection failed: {e}")
            return False
    
    def connect_smtp(self) -> bool:
        """Connect to SMTP server"""
        try:
            if self.config.use_ssl:
                self.smtp_connection = smtplib.SMTP_SSL(
                    self.config.smtp_server, 
                    self.config.smtp_port
                )
            else:
                self.smtp_connection = smtplib.SMTP(
                    self.config.smtp_server, 
                    self.config.smtp_port
                )
                self.smtp_connection.starttls()
            
            self.smtp_connection.login(
                self.config.username, 
                self.config.password
            )
            return True
        except Exception as e:
            print(f"SMTP connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from email servers"""
        if self.imap_connection:
            try:
                self.imap_connection.close()
                self.imap_connection.logout()
            except:
                pass
        
        if self.smtp_connection:
            try:
                self.smtp_connection.quit()
            except:
                pass
    
    def search_emails(self, 
                     folder: str = "INBOX",
                     search_criteria: str = "ALL",
                     since_days: int = 7) -> List[str]:
        """Search for emails matching criteria"""
        if not self.imap_connection:
            if not self.connect_imap():
                return []
        
        try:
            # Select folder
            self.imap_connection.select(folder)
            
            # Calculate date for search
            since_date = (datetime.now() - timedelta(days=since_days)).strftime("%d-%b-%Y")
            search_query = f"(SINCE {since_date})"
            
            # Add support-related keywords to search
            support_keywords = ["support", "query", "request", "help", "issue", "problem"]
            keyword_query = " OR ".join([f'SUBJECT "{keyword}"' for keyword in support_keywords])
            search_query = f"({search_query}) AND ({keyword_query})"
            
            # Search for emails
            status, messages = self.imap_connection.search(None, search_query)
            
            if status == 'OK':
                return messages[0].split()
            else:
                return []
                
        except Exception as e:
            print(f"Email search failed: {e}")
            return []
    
    def fetch_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific email by ID"""
        if not self.imap_connection:
            if not self.connect_imap():
                return None
        
        try:
            # Fetch email
            status, msg_data = self.imap_connection.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                return None
            
            # Parse email
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            
            # Extract email data
            email_data = {
                'id': email_id.decode(),
                'sender': self._extract_sender(email_message),
                'subject': self._extract_subject(email_message),
                'body': self._extract_body(email_message),
                'date': self._extract_date(email_message),
                'raw_message': raw_email.decode('utf-8', errors='ignore')
            }
            
            return email_data
            
        except Exception as e:
            print(f"Email fetch failed: {e}")
            return None
    
    def fetch_emails(self, 
                    folder: str = "INBOX",
                    since_days: int = 7,
                    limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch multiple emails"""
        email_ids = self.search_emails(folder, since_days=since_days)
        
        if not email_ids:
            return []
        
        # Limit results
        email_ids = email_ids[:limit]
        
        emails = []
        for email_id in email_ids:
            email_data = self.fetch_email(email_id)
            if email_data:
                emails.append(email_data)
        
        return emails
    
    def send_email(self, 
                  to_email: str,
                  subject: str,
                  body: str,
                  reply_to: Optional[str] = None) -> bool:
        """Send an email"""
        if not self.smtp_connection:
            if not self.connect_smtp():
                return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if reply_to:
                msg['Reply-To'] = reply_to
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            text = msg.as_string()
            self.smtp_connection.sendmail(
                self.config.username, 
                to_email, 
                text
            )
            
            return True
            
        except Exception as e:
            print(f"Email send failed: {e}")
            return False
    
    def _extract_sender(self, email_message) -> str:
        """Extract sender email address"""
        sender = email_message.get('From', '')
        if '<' in sender and '>' in sender:
            return re.search(r'<(.+?)>', sender).group(1)
        return sender
    
    def _extract_subject(self, email_message) -> str:
        """Extract email subject"""
        subject = email_message.get('Subject', '')
        # Decode subject if needed
        if subject.startswith('=?'):
            decoded_parts = email.header.decode_header(subject)
            subject = ''.join([part[0].decode(part[1] or 'utf-8') 
                             if isinstance(part[0], bytes) 
                             else part[0] for part in decoded_parts])
        return subject
    
    def _extract_body(self, email_message) -> str:
        """Extract email body text"""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return body
    
    def _extract_date(self, email_message) -> str:
        """Extract email date"""
        date_str = email_message.get('Date', '')
        try:
            # Parse email date
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_str)
            return dt.isoformat()
        except:
            return datetime.now().isoformat()

# Email provider configurations
GMAIL_CONFIG = EmailConfig(
    provider="gmail",
    imap_server="imap.gmail.com",
    imap_port=993,
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="",  # Set via environment variables
    password="",  # Set via environment variables
    use_ssl=True
)

OUTLOOK_CONFIG = EmailConfig(
    provider="outlook",
    imap_server="outlook.office365.com",
    imap_port=993,
    smtp_server="smtp.office365.com",
    smtp_port=587,
    username="",  # Set via environment variables
    password="",  # Set via environment variables
    use_ssl=True
)

def get_email_service(provider: str = "gmail") -> EmailService:
    """Get email service for specified provider"""
    if provider.lower() == "gmail":
        config = GMAIL_CONFIG
        config.username = os.getenv("GMAIL_USERNAME", "")
        config.password = os.getenv("GMAIL_PASSWORD", "")
    elif provider.lower() == "outlook":
        config = OUTLOOK_CONFIG
        config.username = os.getenv("OUTLOOK_USERNAME", "")
        config.password = os.getenv("OUTLOOK_PASSWORD", "")
    else:
        raise ValueError(f"Unsupported email provider: {provider}")
    
    return EmailService(config)



