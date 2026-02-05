# Phase 0: Research & Technical Decisions

**Feature**: Phase 1 Backend Skeleton  
**Date**: 2025-11-23  
**Purpose**: Document technology choices, architectural patterns, and implementation decisions

## Overview

This document captures research findings and technical decisions made during Phase 0 planning. Each decision includes rationale, alternatives considered, and references to constitution principles.

---

## 1. Web Framework Selection

### Decision: FastAPI

**Rationale**:
- **Performance**: ASGI-based async framework with excellent performance (comparable to Node.js/Go)
- **Type Safety**: Built-in Pydantic validation aligns with Security-First principle (input validation)
- **Documentation**: Auto-generates OpenAPI/Swagger docs (Observability principle)
- **Modern Python**: Leverages Python 3.11+ type hints and async/await
- **Developer Experience**: Minimal boilerplate, clear error messages
- **Testing**: Excellent test client support via httpx

**Alternatives Considered**:
- **Flask**: More mature but synchronous, lacks built-in validation
- **Django**: Too heavy for API-only service, includes unnecessary ORM/admin features
- **Sanic**: Similar performance but smaller community, less documentation

**Constitution Alignment**: API-First Design, Observability, Security-First

**References**:
- https://fastapi.tiangolo.com/
- Performance benchmarks: https://www.techempower.com/benchmarks/

---

## 2. Database Selection

### Decision: PostgreSQL 15+

**Rationale**:
- **Reliability**: ACID-compliant, battle-tested for production workloads
- **JSON Support**: Native JSONB for spectral data storage (Phase 1)
- **UUID Support**: Built-in UUID type for primary keys
- **Free & Open Source**: Zero-cost development principle
- **Migration Path**: Can scale to cloud-managed instances (RDS, etc.) in Phase 4
- **SQLAlchemy Support**: Excellent ORM integration

**Alternatives Considered**:
- **MySQL**: Less robust JSON support, no native UUID type
- **SQLite**: Not suitable for concurrent writes (Phase 1 needs 50+ concurrent users)
- **MongoDB**: Overkill for structured relational data, adds complexity

**Constitution Alignment**: Zero-Cost Development, Data Integrity

**Data Storage Decision**:
- **Phase 1**: Store spectral points as JSONB array in Sample table
- **Phase 2+**: Consider separate SpectralPoint table if query performance degrades

---

## 3. Authentication Strategy

### Decision: JWT (JSON Web Tokens) with Bcrypt Password Hashing

**Rationale**:
- **Stateless**: Aligns with API-First principle, enables horizontal scaling
- **Industry Standard**: Widely adopted, well-understood security model
- **Library Support**: python-jose provides robust JWT implementation
- **No Session Storage**: Eliminates Redis dependency for auth (use Redis for other caching)
- **Secure**: Bcrypt is industry-standard for password hashing (OWASP recommended)

**Token Structure**:
```json
{
  "sub": "user_uuid",
  "role": "user",
  "exp": 1732383600
}
```

**Security Decisions**:
- Token expiration: 60 minutes (configurable via JWT_EXPIRATION_MINUTES)
- Minimum password length: 8 characters (can be increased later)
- Bcrypt rounds: 12 (balance between security and performance)
- Secret rotation: Manual for Phase 1, automated in Phase 4

**Alternatives Considered**:
- **Session-based auth**: Requires Redis for session storage, not stateless
- **OAuth2**: Overkill for Phase 1, no external providers needed yet
- **API Keys**: Less flexible than JWT for role-based access (Phase 3)

**Constitution Alignment**: Security-First (NON-NEGOTIABLE), API-First

**References**:
- JWT RFC: https://datatracker.ietf.org/doc/html/rfc7519
- OWASP password storage: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

---

## 4. ORM Selection

### Decision: SQLAlchemy 2.0+

**Rationale**:
- **Type Safety**: SQLAlchemy 2.0 adds better type hinting support
- **Async Support**: Native async/await with asyncpg driver
- **Migration Tool**: Alembic (built by SQLAlchemy team) for schema evolution
- **Relationship Handling**: Excellent support for foreign keys, joins
- **SQL Injection Prevention**: Parameterized queries by default
- **Raw SQL Option**: Can drop to raw SQL for complex queries if needed

**Async vs Sync**:
- **Decision**: Use async SQLAlchemy for consistency with FastAPI async endpoints
- **Trade-off**: Slightly more complex setup, but better performance under load

**Alternatives Considered**:
- **Tortoise ORM**: Less mature, smaller community
- **Raw SQL**: More control but more boilerplate, higher SQL injection risk
- **Django ORM**: Tied to Django framework, not usable standalone

**Constitution Alignment**: Security-First (SQL injection prevention), Test-Driven (easier mocking)

---

## 5. File Upload Handling

### Decision: In-Memory CSV Parsing with Size Limit

**Rationale**:
- **Simplicity**: Read CSV into memory, validate, store in database (Phase 1)
- **Size Limit**: 10MB max file size prevents memory exhaustion
- **Future Path**: Can move to streaming/chunked uploads in Phase 2 if needed
- **Database Storage**: Store spectral data as JSONB in Sample table (Phase 1)

**CSV Format**:
```csv
wavelength,absorbance
400.0,0.123
401.0,0.125
...
```

**Validation Rules**:
- Required columns: wavelength, absorbance
- Numeric values only
- Wavelength range: 200-2500 nm (configurable)
- Maximum rows: 10,000 data points per sample

**Alternatives Considered**:
- **S3 Storage**: Adds external dependency, unnecessary for Phase 1
- **Local File System**: Complicates Docker deployment, not cloud-ready
- **Streaming Parser**: More complex, not needed for 10MB limit

**Constitution Alignment**: Phased Delivery (simple solution first), Zero-Cost Development

---

## 6. Caching Strategy

### Decision: Redis for Future Session/Cache Needs

**Rationale**:
- **Phase 1**: Redis container added but not actively used (preparation for Phase 2+)
- **JWT Auth**: Stateless, no session storage needed in Phase 1
- **Future Uses**: 
  - Rate limiting (Phase 2)
  - Caching expensive chemometric computations (Phase 2)
  - Real-time results polling (Phase 3)

**Configuration**:
- Redis 7+ Docker container
- Default Redis config (no persistence needed in Phase 1)
- Connection via redis-py client library

**Alternatives Considered**:
- **No Redis**: Could skip for Phase 1, but adds setup later
- **Memcached**: Less feature-rich than Redis, no data structures
- **In-Memory Python Dict**: Not shared across worker processes

**Constitution Alignment**: Phased Delivery (prepare infrastructure even if not actively used)

---

## 7. Testing Strategy

### Decision: pytest with pytest-asyncio and httpx

**Rationale**:
- **pytest**: Industry standard for Python testing, excellent fixture system
- **pytest-asyncio**: Enables testing async FastAPI endpoints
- **httpx**: FastAPI TestClient uses httpx, allows async HTTP calls
- **Coverage**: pytest-cov for code coverage reporting
- **Database**: Separate test database, rollback after each test

**Test Structure**:
```
tests/
├── unit/           # Fast, isolated tests (no DB)
├── integration/    # API endpoint tests (with test DB)
└── conftest.py     # Shared fixtures
```

**Test Database Strategy**:
- Separate PostgreSQL database: `integrity_test`
- SQLAlchemy session fixtures with rollback
- Alembic migrations applied before test run
- Fast test execution via in-memory tables where possible

**Coverage Target**: 80% minimum for merge to dev

**Alternatives Considered**:
- **unittest**: More verbose, less features than pytest
- **FastAPI TestClient without fixtures**: Less reusable, more boilerplate

**Constitution Alignment**: Test-Driven Development (NON-NEGOTIABLE)

**References**:
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/
- FastAPI testing: https://fastapi.tiangolo.com/tutorial/testing/

---

## 8. Containerization Approach

### Decision: Docker with docker-compose for local development

**Rationale**:
- **Consistency**: Same environment for all developers and CI
- **Zero Setup**: `docker-compose up` starts all services
- **Production-Ready**: Dockerfile can be used in production (Heroku, Kubernetes)
- **Service Isolation**: Backend, PostgreSQL, Redis in separate containers
- **Volume Mounts**: Database persistence via named volumes

**docker-compose.yml Services**:
- `backend`: FastAPI application (port 8000)
- `postgres`: PostgreSQL 15 (port 5432)
- `redis`: Redis 7 (port 6379)

**Environment Variables**:
- `.env` file for local development (not committed)
- `.env.example` with placeholder values (committed)
- CI uses environment variables from GitHub Secrets

**Alternatives Considered**:
- **Virtual environment only**: Requires manual PostgreSQL/Redis installation
- **Podman**: Less adoption than Docker, compatibility issues
- **Bare metal**: Not portable across developer machines

**Constitution Alignment**: Zero-Cost Development, Phased Delivery (production-ready from day 1)

---

## 9. CI/CD Pipeline

### Decision: GitHub Actions with pytest and Docker build

**Rationale**:
- **Free Tier**: GitHub Actions is free for public repositories
- **Integration**: Native GitHub integration, no external services
- **Matrix Testing**: Can test multiple Python versions (future)
- **Docker Build**: Validates Dockerfile builds successfully

**Pipeline Stages**:
1. **Checkout Code**
2. **Set up Python** 3.11
3. **Install Dependencies** (pip install -r requirements.txt)
4. **Run Linter** (flake8 or ruff)
5. **Run Tests** (pytest with coverage)
6. **Build Docker Image**
7. **Report Coverage** (optional: upload to Codecov)

**Trigger**: Pull requests to `dev` and `main`, pushes to `dev`

**Alternatives Considered**:
- **Travis CI**: Not free for private repos
- **CircleCI**: Free tier more limited than GitHub Actions
- **GitLab CI**: Would require migrating to GitLab

**Constitution Alignment**: Test-Driven Development, Zero-Cost Development

---

## 10. Mock Analysis Logic (Phase 1)

### Decision: Simple Heuristic-Based Placeholder

**Rationale**:
- **Phase 1 Scope**: Real chemometric models are Phase 2
- **Transparency**: Clearly document this as mock logic
- **Demonstration**: Shows end-to-end flow without ML complexity

**Mock Algorithm**:
```python
def generate_mock_result(spectral_data):
    # Placeholder logic for Phase 1
    num_points = len(spectral_data)
    avg_absorbance = sum(point['absorbance'] for point in spectral_data) / num_points
    
    # Simple heuristic: high absorbance = authentic
    if avg_absorbance > 0.5:
        status = "Authentic"
        confidence = random.uniform(0.85, 0.95)
    else:
        status = "Suspect"
        confidence = random.uniform(0.60, 0.80)
    
    return {
        "status": status,
        "confidence": round(confidence, 2),
        "model_version": "mock-v1.0",
        "summary": "Phase 1 mock result. Real analysis in Phase 2."
    }
```

**Database Design**:
- Result table includes `model_version` field for Phase 2 tracking
- Summary field documents mock nature

**Alternatives Considered**:
- **No analysis**: Just store samples, add analysis later (less demonstrable)
- **Random only**: Current approach adds minimal heuristic for realism

**Constitution Alignment**: Data Integrity & Scientific Rigor (transparently mock), Phased Delivery

---

## 11. Error Handling & Logging

### Decision: Python logging module with structured JSON logs

**Rationale**:
- **Standard Library**: No additional dependencies
- **Levels**: INFO for operations, ERROR for failures, DEBUG for development
- **Structured**: JSON format for easy parsing (production monitoring)
- **Sentry Integration**: Environment variable enables Sentry (optional)

**Log Format**:
```json
{
  "timestamp": "2025-11-23T16:40:00Z",
  "level": "INFO",
  "message": "User registered",
  "user_id": "uuid-here",
  "endpoint": "/auth/register"
}
```

**Error Response Format**:
```json
{
  "status_code": 400,
  "message": "Invalid email format",
  "detail": "Email must be valid RFC 5322 format"
}
```

**Security Considerations**:
- Never log passwords or JWT secrets
- Sanitize stack traces (don't expose internal paths)
- Rate limit error responses (future: implement in Phase 2)

**Alternatives Considered**:
- **Print statements**: Not production-ready
- **Third-party logger (loguru)**: Additional dependency, Python logging sufficient

**Constitution Alignment**: Observability & Transparency, Security-First

---

## 12. Environment Variable Management

### Decision: python-dotenv with .env files

**Rationale**:
- **12-Factor App**: Configuration via environment variables
- **Development**: `.env` file for local development
- **Production**: Environment variables from container orchestrator
- **Security**: `.env` in `.gitignore`, `.env.example` committed

**Required Environment Variables**:
```bash
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/integrity
# Redis
REDIS_URL=redis://redis:6379/0
# JWT
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
# Application
APP_ENV=development  # development, production
DEBUG=true
# Optional
SENTRY_DSN=
```

**Validation**:
- Pydantic Settings for type-safe config
- Application fails fast if required vars missing
- Clear error messages for misconfiguration

**Alternatives Considered**:
- **Config files**: Less secure, harder to manage across environments
- **Hardcoded values**: Violates Security-First principle

**Constitution Alignment**: Security-First (no hardcoded secrets), Phased Delivery

---

## Summary of Technical Decisions

| Area | Technology | Rationale |
|------|-----------|-----------|
| Web Framework | FastAPI 0.104+ | Performance, type safety, auto-docs |
| Database | PostgreSQL 15+ | ACID compliance, JSON support, free |
| Cache | Redis 7+ | Future-ready, industry standard |
| ORM | SQLAlchemy 2.0+ (async) | Type safety, migrations, async support |
| Authentication | JWT + Bcrypt | Stateless, industry standard, secure |
| Testing | pytest + httpx | Python standard, async support |
| Containerization | Docker + docker-compose | Consistency, zero-setup |
| CI/CD | GitHub Actions | Free, integrated, Docker support |
| Logging | Python logging (JSON) | Standard library, structured |
| Config | python-dotenv | 12-factor app, secure |

All decisions align with project constitution principles:
- ✅ Security-First Development
- ✅ Zero-Cost Development
- ✅ Test-Driven Development  
- ✅ API-First Design
- ✅ Phased Delivery
- ✅ Observability

---

**Phase 0 Complete** - Ready to proceed to Phase 1: Design & Contracts
