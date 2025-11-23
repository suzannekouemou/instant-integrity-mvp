# Quick Start Guide: Phase 1 Backend

**Feature**: Phase 1 Backend Skeleton  
**Date**: 2025-11-23  
**Estimated Setup Time**: 10-15 minutes

## Prerequisites

### Required Software

- **Docker Desktop** 4.20+ ([Download](https://www.docker.com/products/docker-desktop/))
  - Includes Docker and docker-compose
  - Available for Windows, macOS, Linux
- **Git** 2.30+ (for cloning repository)
- **Curl** or **Postman** (for API testing)

### Optional but Recommended

- **Python 3.11+** (for local development without Docker)
- **VS Code** with Python extension
- **Insomnia** or **Postman** (API testing GUI)

---

## Quick Start (Docker)

### 1. Clone Repository

```bash
git checkout 001-phase1-backend
cd instant-integrity-mvp
```

### 2. Configure Environment

```bash
# Copy example environment file
cp backend/.env.example backend/.env

# Edit .env file with your values (or use defaults for development)
# Required variables:
# - DATABASE_URL
# - REDIS_URL
# - JWT_SECRET (IMPORTANT: Change in production!)
```

**backend/.env** (development defaults):
```bash
DATABASE_URL=postgresql://user:password@postgres:5432/integrity
REDIS_URL=redis://redis:6379/0
JWT_SECRET=change-this-secret-in-production-use-long-random-string
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
APP_ENV=development
DEBUG=true
```

### 3. Start Services

```bash
# Start all services (backend, PostgreSQL, Redis)
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Wait for "Application startup complete" message
```

### 4. Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","database":"connected","redis":"connected","timestamp":"..."}
```

### 5. Access API Documentation

Open in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Testing the API

### Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

Expected response:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

**Save the `access_token` for subsequent requests!**

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### Create Sample CSV File

```bash
cat > sample_test.csv << 'EOF'
wavelength,absorbance
400.0,0.123
401.0,0.125
402.0,0.127
403.0,0.130
404.0,0.132
EOF
```

### Upload Sample

```bash
# Replace YOUR_TOKEN with the access_token from registration/login
curl -X POST http://localhost:8000/api/v1/samples/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample_test.csv"
```

Expected response:
```json
{
  "sample_id": "uuid-here",
  "status": "Authentic",
  "confidence": 0.87,
  "model_version": "mock-v1.0",
  "summary": "Phase 1 mock result. Real analysis in Phase 2."
}
```

### Get Result

```bash
# Replace SAMPLE_ID and YOUR_TOKEN
curl -X GET http://localhost:8000/api/v1/results/SAMPLE_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Development Setup (Local Python)

### 1. Create Virtual Environment

```bash
cd backend
python3.11 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start Database Services

```bash
# Start only PostgreSQL and Redis via Docker
docker-compose up -d postgres redis
```

### 4. Run Database Migrations

```bash
# Apply migrations
alembic upgrade head

# Create new migration (if needed)
alembic revision --autogenerate -m "Description"
```

### 5. Start Development Server

```bash
# With auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m uvicorn app.main:app --reload
```

---

## Running Tests

### All Tests

```bash
cd backend
pytest
```

### With Coverage

```bash
pytest --cov=app --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Specific Test Files

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_security.py

# Specific test function
pytest tests/unit/test_security.py::test_password_hashing
```

### Watch Mode (Development)

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file changes
ptw
```

---

## Common Commands

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Restart backend only
docker-compose restart backend

# Rebuild backend image
docker-compose build backend

# Clean up everything (including volumes)
docker-compose down -v
```

### Database Commands

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U user -d integrity

# View tables
\dt

# Describe table
\d users

# Run query
SELECT * FROM users;

# Exit
\q
```

### Redis Commands

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# View all keys
KEYS *

# Get value
GET key

# Exit
exit
```

---

## Troubleshooting

### Port Already in Use

If port 8000, 5432, or 6379 is already in use:

```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change ports in docker-compose.yml
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### JWT Token Expired

Tokens expire after 60 minutes (default). Login again to get a new token.

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpassword123"}'
```

### Import Errors (Local Development)

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Tests Failing

```bash
# Create test database
docker-compose exec postgres psql -U user -c "CREATE DATABASE integrity_test;"

# Apply migrations to test database
DATABASE_URL=postgresql://user:password@localhost:5432/integrity_test alembic upgrade head

# Run tests
pytest
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `REDIS_URL` | Yes | - | Redis connection string |
| `JWT_SECRET` | Yes | - | Secret key for JWT signing (change in production!) |
| `JWT_ALGORITHM` | No | HS256 | JWT signing algorithm |
| `JWT_EXPIRATION_MINUTES` | No | 60 | Token expiration time |
| `APP_ENV` | No | development | Environment (development/production) |
| `DEBUG` | No | false | Enable debug mode |
| `SENTRY_DSN` | No | - | Sentry error tracking (optional) |
| `MAX_UPLOAD_SIZE` | No | 10485760 | Max file upload size in bytes (10MB) |
| `CORS_ORIGINS` | No | * | Allowed CORS origins (comma-separated) |

---

## Next Steps

1. **Read API Documentation**: http://localhost:8000/docs
2. **Review Data Model**: [data-model.md](./data-model.md)
3. **Check API Contracts**: [contracts/api-summary.md](./contracts/api-summary.md)
4. **Run Tests**: `pytest --cov=app`
5. **Explore Code**: Start with `backend/app/main.py`

---

## Getting Help

- **Issue Tracker**: GitHub Issues
- **Documentation**: `/specs/001-phase1-backend/` directory
- **API Docs**: http://localhost:8000/docs

---

**Setup Complete!** 🎉 You now have a fully functional Phase 1 backend running locally.
