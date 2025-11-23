# Key Decisions Reference

**Feature**: Phase 1 Backend Skeleton  
**Date**: 2025-11-23

Quick reference for all major decisions made during planning.

---

## Critical Additions (Moved from Out of Scope)

| Feature | Decision | Rationale | Impact |
|---------|----------|-----------|--------|
| **Rate Limiting** | ✅ Include in Phase 1 | Security-First principle (NON-NEGOTIABLE) | +6 req, +1 day |
| **Email Verification** | ✅ Include in Phase 1 | Prevents fake accounts, enables password reset | +5 req, +2 days |
| **Sentry Integration** | ✅ Include in Phase 1 | Observability principle | +3 req, +0.5 day |
| **Sample Types** | ✅ Include in Phase 1 | Multi-industry, prevents migration | +3 req, +0.5 day |
| **Integration Tests in CI** | ✅ Include in Phase 1 | TDD principle | +CI time |

**Total Impact**: +18 requirements, +7 days effort (justified for production-ready)

---

## Technology Stack

| Component | Choice | Alternatives Rejected | Why Chosen |
|-----------|--------|----------------------|------------|
| **Language** | Python 3.11+ | - | Modern async, type hints |
| **Framework** | FastAPI 0.104+ | Flask, Django | Async, auto-docs, performance |
| **Database** | PostgreSQL 15+ | MongoDB, MySQL | ACID, JSONB, tooling |
| **ORM** | SQLAlchemy 2.0+ async | Django ORM, Raw SQL | Type safety, migrations |
| **Auth** | JWT + Bcrypt | Sessions, OAuth | Stateless, industry standard |
| **Rate Limiting** | slowapi 0.1.9+ | fastapi-limiter | FastAPI-native, Redis-backed |
| **Email** | SendGrid (free) + SMTP | AWS SES, Mailgun | 5k/month free, simple |
| **Error Tracking** | Sentry SDK | Log aggregation only | Free tier, aggregation |
| **Cache** | Redis 7+ | Memcached | Rate limiting + future sessions |
| **Container** | Docker + compose | Manual setup | Zero-setup, consistent |
| **CI/CD** | GitHub Actions | CircleCI, Travis | Free tier, native integration |

---

## Database Schema Decisions

### User Model
- ✅ UUID primary keys (better distributed systems)
- ✅ email_verified boolean (Phase 1 addition)
- ✅ Bcrypt password hash (12 rounds minimum)
- ✅ Role field (future RBAC in Phase 3)

### EmailVerificationToken Model (NEW)
- ✅ Separate table (not JSON in User)
- ✅ 24-hour expiration
- ✅ One-time use flag
- ✅ Token is URL-safe string

### Sample Model
- ✅ JSONB for spectral data (flexibility)
- ✅ sample_type enum (Phase 1 addition)
- ✅ Metadata as JSONB (extensible)
- ✅ Foreign key to User (ownership)

### Result Model
- ✅ One-to-one with Sample (unique constraint)
- ✅ model_version field (Phase 2 versioning)
- ✅ Confidence as float 0-1
- ✅ Status enum (Authentic/Suspect/Verify)

---

## API Design Decisions

### Endpoints
1. POST `/api/v1/auth/register` - Rate limited: 3/hour per IP
2. GET `/api/v1/auth/verify-email` - Token in query param (NEW)
3. POST `/api/v1/auth/login` - Rate limited: 5/min per IP
4. POST `/api/v1/samples/upload` - Rate limited: 10/hour per user
5. GET `/api/v1/results/{sample_id}` - Authorization check
6. GET `/health` - No auth required
7. GET `/docs` - OpenAPI auto-generated

### Rate Limiting Strategy
- ✅ Per-IP for public endpoints (register, login)
- ✅ Per-user for authenticated (upload)
- ✅ Redis-backed counters with expiration
- ✅ HTTP 429 + Retry-After header
- ✅ Rate limit headers on all responses

### Authentication Flow
1. Register → Email sent with token
2. Verify email via token link
3. Login → Check email_verified → Return JWT
4. Protected endpoints → Validate JWT

---

## Environment Variables

### Required
```bash
DATABASE_URL=postgresql://user:password@postgres:5432/integrity
REDIS_URL=redis://redis:6379/0
JWT_SECRET=change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
```

### Email (choose one)
```bash
SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
# OR
SENDGRID_API_KEY=SG.xxx
FROM_EMAIL=noreply@instantintegrity.com
VERIFICATION_TOKEN_EXPIRY_HOURS=24
```

### Rate Limiting
```bash
RATE_LIMIT_ENABLED=true
```

### Sentry (optional)
```bash
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=development
```

---

## Testing Strategy

### Unit Tests
- All services (auth, email, analysis)
- Security functions (JWT, bcrypt)
- Utilities (CSV parser, token generation)
- **Target**: 80%+ coverage

### Integration Tests
- All API endpoints
- Rate limiting enforcement
- Email verification flow
- Authorization checks
- **Run in CI**: Both unit + integration

### Test Infrastructure
- pytest + pytest-asyncio
- httpx for API testing
- Separate test database
- Fixtures for common setup

---

## Deferred to Later Phases

### Phase 2
- Real ML models
- Advanced rate limiting (IP blocking, exponential backoff)
- Advanced email features (templates, bounce handling)
- Advanced Sentry (performance monitoring)

### Phase 3
- Frontend (Next.js)
- Role-based access control
- Password reset (uses Phase 1 email verification)

### Phase 4
- Cloud deployment
- Production email service upgrade
- Database backups
- Performance testing

---

## Trade-offs Made

| Decision | Pro | Con | Accepted Because |
|----------|-----|-----|------------------|
| JWT auth | Stateless, scalable | Can't revoke instantly | Short expiry mitigates |
| JSONB for spectral data | Flexible schema | Harder to query | Phase 1 simplicity |
| SendGrid free tier | Zero cost | Vendor lock-in | Easy to switch later |
| Rate limit per IP | Simple | VPN/NAT issues | Phase 1 acceptable |
| Mock analysis | Fast to implement | Not real value | Transparent placeholder |
| Email in Phase 1 | Production-ready | +2 days effort | Prevents fake accounts |

---

## Success Metrics

### Phase 1 Completion
- ✅ All 56 requirements implemented
- ✅ 93 tasks checked off
- ✅ 80%+ test coverage
- ✅ CI pipeline green
- ✅ Docker compose up works

### MVP (US2) Completion
- ✅ User registration with email verification
- ✅ Secure login with JWT
- ✅ Rate limiting enforced
- ✅ ~12-15 days effort

### Performance
- Registration: < 30 seconds
- Login: < 2 seconds
- Upload + analysis: < 5 seconds
- Error responses: < 1 second

---

## Quick Reference URLs

**Documentation**:
- Spec: `specs/001-phase1-backend/spec.md`
- Plan: `specs/001-phase1-backend/plan.md`
- Tasks: `specs/001-phase1-backend/tasks.md`
- Session Log: `specs/001-phase1-backend/SESSION_LOG.md`

**External**:
- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy: https://docs.sqlalchemy.org/en/20/
- Pydantic: https://docs.pydantic.dev
- slowapi: https://github.com/laurents/slowapi
- SendGrid: https://sendgrid.com/docs
- Sentry: https://docs.sentry.io/platforms/python/guides/fastapi/

---

*Last Updated: 2025-11-23*
