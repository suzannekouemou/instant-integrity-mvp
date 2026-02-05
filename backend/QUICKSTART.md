# Quick Start Guide - Instant Integrity Backend

## Prerequisites
- Docker and docker-compose installed
- Git

## Setup (5 minutes)

### 1. Clone and Configure
```bash
git clone <repository-url>
cd instant-integrity-mvp
cp backend/.env.example backend/.env
```

### 2. Start Services
```bash
docker-compose up -d
```

### 3. Run Migrations
```bash
docker-compose exec backend alembic upgrade head
```

### 4. Verify Installation
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "healthy",
  "redis": "healthy"
}
```

## Usage Examples

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### 2. Verify Email (use token from email/logs)
```bash
curl "http://localhost:8000/api/v1/auth/verify-email?token=YOUR_TOKEN"
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

Save the `access_token` from response.

### 4. Upload Sample
```bash
curl -X POST http://localhost:8000/api/v1/samples/upload \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@sample.csv" \
  -F "sample_type=flour"
```

### 5. Get Result
```bash
curl http://localhost:8000/api/v1/results/SAMPLE_ID \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## API Documentation

Interactive documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Services not starting
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f
```

### Database connection issues
```bash
docker-compose exec postgres psql -U user -d integrity
```

### Reset everything
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## Development

### Run tests
```bash
docker-compose exec backend pytest
```

### View logs
```bash
docker-compose logs -f backend
```

### Access database
```bash
docker-compose exec postgres psql -U user -d integrity
```

## Next Steps

1. Explore API at http://localhost:8000/docs
2. Review constitution at `.specify/memory/constitution.md`
3. Check Phase 2 planning for chemometric models
