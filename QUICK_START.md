# Quick Start Guide

## 1. Environment Setup

Create a `.env` file in the project root:

```env
# Database Configuration (required for full functionality)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app
DB_USER=postgres
DB_PASSWORD=your_password_here

# Security (required)
SECRET_KEY=your_super_secret_key_here_change_in_production
ALGORITHM=HS256

# Ollama Configuration (optional - will use mock embeddings if not available)
OLLAMA_URL=http://localhost:11434/api/generate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Start the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **ReDoc**: http://localhost:8000/redoc

## 5. Database Setup (Optional)

If you want full functionality:

1. Install PostgreSQL with pgvector extension
2. Create database: `CREATE DATABASE app;`
3. Set environment variables in `.env`
4. Restart the application

## 6. Ollama Setup (Optional)

For AI embeddings:

```bash
# Install Ollama
# Then pull the required model
ollama pull nomic-embed-text
```

## 7. Test the API

The app will start without database or Ollama - you can test the API endpoints and see mock responses.

### Example API Usage:

```bash
# Health check
curl http://localhost:8000/health

# Sign up user
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"TestPass123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123"}'
```

## Notes

- The app starts successfully even without database connection
- Without database, endpoints will return appropriate error messages
- Without Ollama, AI features use mock embeddings
- All logging is saved to `logs/app_YYYYMMDD.log`
- Error handling provides consistent JSON error responses
