# EmailAce AI Backend

AI-powered email communication assistant backend built with FastAPI, SQLAlchemy, and HuggingFace transformers.

## 🚀 Features

- **AI Email Processing**: Sentiment analysis, urgency detection, entity extraction
- **Smart Reply Generation**: Context-aware automated reply suggestions
- **Email Management**: CRUD operations with intelligent categorization
- **Analytics Dashboard**: Comprehensive email statistics and insights
- **RESTful API**: Clean, documented endpoints for frontend integration

## 🛠️ Tech Stack

- **Framework**: FastAPI + Uvicorn
- **Database**: SQLite + SQLAlchemy ORM
- **AI Models**: HuggingFace Transformers (DistilBERT, T5)
- **Language**: Python 3.8+

## 📦 Installation

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model** (optional, for enhanced NER):
   ```bash
   python -m spacy download en_core_web_sm
   ```

## 🏃‍♂️ Running the Backend

### Development Mode
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Direct Python Execution
```bash
python main.py
```

## 📚 API Documentation

Once running, visit: **http://127.0.0.1:8000/docs**

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/` | Health check |
| `GET` | `/api/v1/emails` | Get all emails |
| `GET` | `/api/v1/emails/{id}` | Get email details |
| `POST` | `/api/v1/emails/{id}/generate-reply` | Generate AI reply |
| `POST` | `/api/v1/emails/{id}/send-reply` | Mark as resolved |
| `GET` | `/api/v1/analytics` | Get email statistics |
| `POST` | `/api/v1/emails/{id}/archive` | Archive email |
| `GET` | `/api/v1/emails/search/{query}` | Search emails |

## 🗄️ Database Schema

### Emails Table
- `id`: Primary key
- `sender`: Email sender address
- `subject`: Email subject line
- `body`: Email content
- `date`: Timestamp
- `sentiment`: AI-detected sentiment (positive/negative/neutral)
- `priority`: Urgency level (urgent/high/normal/low)
- `status`: Processing status (pending/resolved/archived)
- `draft_reply`: AI-generated reply suggestion
- `is_urgent`: Boolean urgency flag
- `summary`: AI-generated email summary
- `entities`: Extracted entities (JSON)

## 🤖 AI Features

### 1. Sentiment Analysis
- **Model**: DistilBERT base uncased SST-2
- **Output**: Positive, Negative, Neutral
- **Use Case**: Customer satisfaction tracking

### 2. Urgency Detection
- **Method**: Keyword-based analysis
- **Keywords**: urgent, critical, immediately, asap, emergency
- **Output**: Priority levels and urgency flags

### 3. Entity Extraction
- **Patterns**: Email addresses, phone numbers, URLs
- **Output**: Structured entity data for contact management

### 4. Summarization
- **Model**: T5-small
- **Output**: Concise email summaries
- **Use Case**: Quick content overview

### 5. Reply Generation
- **Method**: Template-based + context awareness
- **Input**: Email content, sentiment, urgency
- **Output**: Professional reply suggestions

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=sqlite:///./emailace.db
MODEL_CACHE_DIR=./models
```

### CORS Settings
Frontend origins are configured in `main.py`:
```python
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

## 📊 Sample Data

The system automatically seeds the database with 10 realistic sample emails:
- Urgent server issues
- Customer feedback (positive/negative)
- Meeting requests
- Policy updates
- System maintenance notices

## 🔗 Frontend Integration

### Axios Example
```javascript
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

// Get all emails
const emails = await axios.get(`${API_BASE}/emails`);

// Generate AI reply
const reply = await axios.post(`${API_BASE}/emails/1/generate-reply`);

// Get analytics
const analytics = await axios.get(`${API_BASE}/analytics`);
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Kill process on port 8000
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

2. **Model download issues**:
   ```bash
   # Clear cache and retry
   pip cache purge
   pip install -r requirements.txt --no-cache-dir
   ```

3. **Database errors**:
   ```bash
   # Remove and recreate database
   rm emailace.db
   python main.py
   ```

## 📈 Performance Notes

- **First Run**: Models download (~500MB) - may take time
- **Subsequent Runs**: Models loaded from cache
- **Memory Usage**: ~2GB RAM recommended for optimal performance
- **Response Time**: AI processing typically 1-3 seconds per email

## 🎯 Hackathon Ready Features

- ✅ Self-contained setup
- ✅ Sample data included
- ✅ Comprehensive API
- ✅ AI processing pipeline
- ✅ Clean code structure
- ✅ CORS configured
- ✅ Documentation included

## 🤝 Contributing

This is a hackathon project. Feel free to:
- Add new AI models
- Enhance entity extraction
- Improve reply generation
- Add authentication
- Implement real email integration

## 📄 License

MIT License - Hackathon Project


