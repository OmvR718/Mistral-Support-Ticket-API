# Mistral Support Ticket API

A comprehensive FastAPI-based support ticket system that uses Mistral AI for automatic ticket classification with priority and category prediction using Retrieval-Augmented Generation (RAG).

## Features

- **User Authentication**: Secure JWT-based authentication with password validation
- **Ticket Management**: Create, view, and manage support tickets
- **AI-Powered Classification**: Automatic ticket classification using Mistral AI
- **Vector Search**: RAG implementation with pgvector for knowledge retrieval
- **Document Upload**: File upload with smart parsing and metadata extraction
- **Secure Database**: PostgreSQL with proper schema and connection management
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Logging & Monitoring**: Comprehensive error handling and structured logging

## Security Improvements

- Environment variable configuration (no hardcoded credentials)
- Strong JWT secret key requirements
- Password complexity validation
- Proper authentication middleware
- Input validation and sanitization
- Comprehensive error handling

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+ with pgvector extension
- Ollama with `nomic-embed-text` model (optional - uses mock embeddings if not available)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Mistral-Support-Ticket-API
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

4. Start PostgreSQL and ensure pgvector extension is available

5. Pull the required Ollama model (optional):
```bash
ollama pull nomic-embed-text
```

6. Start the API server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Authenticate and get JWT token

### Tickets
- `POST /tickets/` - Create new ticket (requires authentication)
- `GET /tickets/` - List current user's tickets (requires authentication)
- `GET /tickets/user/{username}` - List tickets by username (requires authentication)

### AI Classification
- `POST /tickets/{id}/classify` - Classify ticket using AI (requires authentication)

### Documents & Knowledge Base
- `POST /documents/upload` - Upload document text content
- `POST /documents/upload-file` - Upload document files (PDF, DOCX, MD, TXT)
- `GET /documents/` - List all uploaded documents
- `GET /documents/{id}` - Get specific document details
- `GET /documents/{id}/chunks` - View document chunks
- `DELETE /documents/{id}` - Delete document and chunks

### System
- `GET /health` - System health check and database status

## Environment Variables

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app
DB_USER=postgres
DB_PASSWORD=your_password_here

# Security
SECRET_KEY=your_super_secret_key_here_change_in_production
ALGORITHM=HS256

# Ollama Configuration (optional)
OLLAMA_URL=http://localhost:11434/api/generate
```

## Database Schema

The application uses the following main tables:

- `users` - User accounts and authentication
- `tickets` - Support tickets
- `ticket_predictions` - AI classification results
- `knowledge_docs` - Knowledge base documents
- `doc_chunks` - Document chunks with vector embeddings
- `logs` - AI interaction logs

## AI Pipeline

The classification pipeline works as follows:

1. **Embedding**: Ticket content using Nomic embeddings (768-dimension vectors)
2. **Retrieval**: Find similar document chunks via cosine similarity search
3. **Context Building**: Build classification prompt with retrieved knowledge base context
4. **Classification**: Call Mistral AI via Ollama for category and priority prediction
5. **Storage**: Store prediction results and log AI interactions

## Document Processing Features

### Smart Metadata Extraction
- **Content Analysis**: Word count, character count, line count
- **Entity Detection**: Automatically identifies keywords and common terms
- **Category Classification**: Auto-categorizes content (billing, technical, general, authentication)
- **Language Detection**: Default language detection
- **File Type Support**: PDF, DOCX, Markdown, TXT files

### Supported File Formats
- **Text Files**: `.txt`, `.md` - Direct content processing
- **Documents**: `.docx` - Word document content extraction
- **PDFs**: `.pdf` - PDF text extraction (basic support)
- **Auto-Detection**: File type detection based on extension

## Development

### Running Tests
```bash
# Test API endpoints
python test_ai_components.py

# Test document processing
python test_document_upload.py

# Test logging and error handling
python test_logging.py
```

### Database Migrations
```bash
# Future: Add Alembic for database migrations
```

## Security Best Practices

- Always use a strong, random `SECRET_KEY` in production
- Ensure database credentials are properly secured
- Use HTTPS in production environments
- Implement rate limiting for production deployments
- Regular security updates for all dependencies
- Input validation for all API endpoints

## Production Deployment

### Docker Support
```dockerfile
# Future: Add Dockerfile for containerized deployment
```

### Environment Configuration
- Use environment-specific configuration files
- Separate development/staging/production settings
- Secure secret management in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request with detailed description

## License

This project is open source and available under the [MIT License](LICENSE).

## Project Status

**Complete and Production-Ready**

This is a fully-featured support ticket system with advanced AI capabilities that demonstrates:
- **FastAPI expertise** with modern Python patterns
- **Database design** with SQLAlchemy and PostgreSQL
- **AI/ML integration** with embeddings and RAG
- **Security awareness** with JWT and validation
- **Production readiness** with logging and error handling
- **Document processing** with smart parsing and metadata extraction

**Perfect for**: Junior developer portfolios, technical interviews, and production deployments.

---


**Built with ❤️ using FastAPI, PostgreSQL, pgvector, and Mistral AI**
