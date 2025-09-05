# EmailAce AI - AI-Powered Communication Assistant

## 🎬 Demo Video

**Video Link:** https://drive.google.com/file/d/10Rz7zh6dnx8kpsNYb8IHKp7WFa39cmrL/view?usp=sharing

## 🚀 Project Overview

EmailAce AI is a comprehensive AI-powered email management system designed to intelligently handle customer support emails. It automatically analyzes incoming emails, prioritizes them based on urgency, generates context-aware responses using RAG (Retrieval-Augmented Generation), and provides a user-friendly dashboard for email management.

## ✨ Key Features

### Core Functionality
- **Email Retrieval & Filtering**: Fetches emails from Gmail/Outlook with support-related keyword filtering
- **AI-Powered Analysis**: Sentiment analysis, urgency detection, and entity extraction
- **RAG-Enhanced Responses**: Context-aware reply generation using knowledge base
- **Priority Queue**: Intelligent email processing based on urgency levels
- **Real-time Dashboard**: Analytics, email management, and response tracking
- **Email Sending**: Actual email reply functionality

### AI Capabilities
- **Sentiment Analysis**: Positive/Negative/Neutral classification
- **Urgency Detection**: Automatic priority assignment (Urgent/High/Normal/Low)
- **Entity Extraction**: Phone numbers, emails, URLs, and other key information
- **Smart Summarization**: Concise email summaries
- **Context-Aware Responses**: RAG-powered reply generation with knowledge base

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **FastAPI**: RESTful API with automatic documentation
- **SQLAlchemy**: Database ORM with SQLite
- **Hugging Face Transformers**: AI/ML models for text processing
- **Sentence Transformers**: Embeddings for RAG implementation
- **IMAP/SMTP**: Email integration
- **Priority Queue**: Email processing prioritization

### Frontend (React/TypeScript)
- **React 18**: Modern UI framework
- **TypeScript**: Type-safe development
- **shadcn/ui**: Beautiful, accessible components
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Data visualization
- **React Query**: Server state management

## 📋 Requirements Met

### ✅ Email Retrieval & Filtering
- IMAP integration for Gmail/Outlook
- Support keyword filtering ("support", "query", "request", "help")
- Email metadata extraction

### ✅ Categorization & Prioritization
- Sentiment analysis (Positive/Negative/Neutral)
- Urgency detection with keyword matching
- Priority queue implementation
- Urgent emails processed first

### ✅ Context-Aware Auto-Responses
- RAG implementation with knowledge base
- Context-aware reply generation
- Professional tone maintenance
- Empathetic responses for frustrated customers

### ✅ Information Extraction
- Contact details extraction (phone, email)
- Entity recognition and classification
- Metadata extraction for faster processing

### ✅ Dashboard & Analytics
- Real-time email listing with filtering
- Analytics dashboard with charts
- Email volume trends
- Sentiment distribution
- Response time metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gmail/Outlook account with App Password

### Installation

1. **Clone and setup**:
```bash
git clone <repository-url>
cd emailace-ai
python setup.py
```

2. **Configure email credentials**:
```bash
# Edit .env file
GMAIL_USERNAME=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
REPLY_EMAIL=your-reply-email@company.com
```

3. **Start the application**:
```bash
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend
npm run dev
```

4. **Access the application**:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
emailace-ai/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── routes.py            # API endpoints
│   ├── models.py            # Pydantic models
│   ├── database.py          # SQLAlchemy models
│   ├── ai_processor.py      # AI/ML processing
│   ├── email_service.py     # Email integration
│   ├── knowledge_base.py    # RAG implementation
│   ├── priority_queue.py    # Email prioritization
│   └── seed_data.py         # Sample data
├── src/
│   ├── pages/
│   │   └── dashboard/       # Dashboard components
│   ├── components/          # Reusable UI components
│   ├── lib/
│   │   └── api.ts          # API service layer
│   └── App.tsx             # Main application
├── requirements.txt         # Python dependencies
├── package.json            # Node.js dependencies
└── setup.py               # Setup script
```

## 🔧 Configuration

### Email Setup

#### Gmail
1. Enable 2-factor authentication
2. Generate App Password
3. Use App Password in GMAIL_PASSWORD

#### Outlook
1. Enable 2-factor authentication
2. Generate App Password
3. Use App Password in OUTLOOK_PASSWORD

### Environment Variables
```bash
# Email Configuration
GMAIL_USERNAME=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
OUTLOOK_USERNAME=your-email@outlook.com
OUTLOOK_PASSWORD=your-password
REPLY_EMAIL=your-reply-email@company.com

# Database
DATABASE_URL=sqlite:///./emailace.db

# AI APIs (Optional)
OPENAI_API_KEY=your-openai-key
HUGGINGFACE_API_KEY=your-hf-key
```

## 📊 API Endpoints

### Email Management
- `GET /api/v1/emails` - List all emails
- `GET /api/v1/emails/{id}` - Get email details
- `POST /api/v1/emails/sync` - Sync emails from provider
- `POST /api/v1/emails/{id}/generate-reply` - Generate AI reply
- `POST /api/v1/emails/{id}/send-reply` - Send email reply

### Analytics
- `GET /api/v1/analytics` - Get analytics data
- `GET /api/v1/queue/status` - Get priority queue status

## 🎯 Demo Features

### 1. Email Dashboard
- Real-time email listing
- Priority-based sorting
- Sentiment analysis display
- Search and filtering

### 2. AI-Powered Responses
- Context-aware reply generation
- Knowledge base integration
- Sentiment-appropriate tone
- Professional formatting

### 3. Analytics & Insights
- Email volume trends
- Sentiment distribution
- Response time metrics
- Priority breakdown

### 4. Priority Queue
- Urgent email prioritization
- Automatic processing
- Retry mechanism
- Queue status monitoring

## 🔍 Technical Implementation

### RAG (Retrieval-Augmented Generation)
- Knowledge base with support scenarios
- Sentence transformers for embeddings
- Cosine similarity for retrieval
- Context-aware response generation

### Priority Queue
- Heap-based priority queue
- Urgent email processing
- Retry mechanism for failed emails
- Queue status monitoring

### Email Integration
- IMAP for email retrieval
- SMTP for email sending
- Support keyword filtering
- Multi-provider support (Gmail/Outlook)

## 🚀 Future Enhancements

- [ ] Real-time email notifications
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Custom knowledge base management
- [ ] Team collaboration features
- [ ] Email template management
- [ ] Advanced AI model integration

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**EmailAce AI** - Transforming customer support with AI-powered email management! 🚀



