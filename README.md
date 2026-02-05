# Instant Integrity MVP

## Overview

Instant Integrity is a cloud-powered authenticity verification platform that combines **spectroscopy, chemometrics, and AI** to deliver instant, reliable quality control across the supply chain — reducing fraud, saving costs, and raising global standards.

## Vision

A proof-of-concept platform that delivers instant authenticity analysis using spectroscopy data processed through chemometric models, delivered via the cloud for industries like food, herbs, spices, and flour.

## Key Features

- **Data Acquisition**: Integration with handheld and benchtop spectroscopy devices (FTIR, NIR)
- **Cloud-Based Chemometric Analysis**: Noise reduction, PCA, multivariate modeling, AI-powered authenticity predictions
- **Decision Support**: Instant results (seconds), batch-level screening, clear authenticity indicators
- **Supply Chain Integration**: End-to-end visibility, mobile app support, cloud accessibility
- **Business Benefits**: Cost-effective, unlimited testing, reduced carbon footprint, regulatory support

## Technology Stack

### Backend
- **Python 3.11+** with FastAPI
- **PostgreSQL 15+** for data persistence
- **Redis 7+** for caching
- **SQLAlchemy** for ORM
- **Pydantic** for data validation

### ML/Science
- **NumPy, SciPy** for numerical computing
- **scikit-learn** for chemometric models (PCA, classifiers)
- **matplotlib** for visualization

### Security
- **JWT** authentication
- **Bcrypt** password hashing
- **python-jose** for token management

### DevOps
- **Docker** and docker-compose
- **GitHub Actions** for CI/CD
- **Heroku/Render** (optional deployment)

## Project Phases

### Phase 1: Backend Skeleton & Project Setup
- GitHub repository with CI/CD pipeline
- FastAPI backend with JWT authentication
- PostgreSQL + Redis integration
- Mock sample upload endpoint
- Dockerized environment

### Phase 2: Chemometric Model Integration
- Preprocessing pipeline (baseline correction, noise reduction, PCA)
- Simple classifier (authentic vs suspect)
- Real model predictions replacing mock results
- Batch-level analysis endpoints

### Phase 3: Frontend & Supply Chain Workflow
- Next.js + Tailwind dashboard
- Role-based access control
- Batch summaries and reports
- CSV/PDF export functionality

### Phase 4: Scaling & Observability
- Kubernetes deployment manifests
- Prometheus metrics + Grafana dashboards
- Sentry error tracking
- Performance testing and optimization

## Getting Started

### Prerequisites
- Docker and docker-compose
- Git
- Python 3.11+ (for local development)

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd instant-integrity-mvp

# Copy environment file
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration

# Start services with docker-compose
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Access the API documentation
open http://localhost:8000/docs

# Check health
curl http://localhost:8000/health
```

### Development Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your local configuration

# Run database migrations
alembic upgrade head

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `GET /api/v1/auth/verify-email?token=xxx` - Verify email address
- `POST /api/v1/auth/login` - Login and receive JWT token

### Samples (Authenticated)
- `POST /api/v1/samples/upload` - Upload CSV spectral data
  - Requires: JWT token, CSV file, sample_type (flour/spice/herb/other)
  - Returns: Mock authenticity result

### Results (Authenticated)
- `GET /api/v1/results/{sample_id}` - Retrieve analysis result

### System
- `GET /health` - Health check (database and Redis status)
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_security.py

# Run integration tests only
pytest tests/integration/
```

## Branching Strategy

- `main`: Production-ready, stable code
- `dev`: Integration branch for completed features
- `feature/<feature-name>`: Individual feature branches
- `hotfix/<issue>`: Critical fixes

### Workflow

1. Create feature branch from `dev`: `git checkout -b feature/jwt-auth dev`
2. Implement feature with tests
3. Create Pull Request to `dev`
4. After review and CI pass, merge to `dev`
5. Periodically merge `dev` to `main` for releases

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes to core principles or APIs
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, documentation updates

Current Version: **0.1.0** (Phase 1 in progress)

## Contributing

1. Check the constitution at `.specify/memory/constitution.md`
2. Create a GitHub issue for your feature/bug
3. Create a feature branch
4. Write tests first (TDD)
5. Implement feature
6. Submit Pull Request with issue reference

## Documentation

- [Constitution](.specify/memory/constitution.md) - Core principles and governance
- [Proof of Concept Document](Proof%20of%20Concept%20Document.md) - Project vision and architecture
- [Technical Documentation – Phase 1](📄%20Technical%20Documentation%20–%20Phase%201.md) - Detailed Phase 1 specs

## Security

See our [Constitution](.specify/memory/constitution.md) for security principles. Key points:
- JWT authentication required
- No hardcoded secrets
- Bcrypt password hashing
- Input validation on all endpoints
- Audit trails for all operations

## License

MIT License - See LICENSE file for details

## Contact

For questions or support, please create a GitHub issue.

---

**Status**: ✅ Phase 1 Complete (85/93 tasks)  
**Last Updated**: 2025-11-24  
**Next Phase**: Phase 2 - Chemometric Model Integration
