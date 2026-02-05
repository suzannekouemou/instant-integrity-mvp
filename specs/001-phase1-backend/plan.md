# Implementation Plan: Phase 1 Backend Skeleton (UPDATED)

**Branch**: `001-phase1-backend` | **Date**: 2025-11-23 (Updated) | **Spec**: [spec.md](./spec.md)

**Note**: This plan reflects the updated specification after clarification. Requirements increased from 38 to 56.

## Summary

Phase 1 delivers a **production-ready** backend with:
- FastAPI REST API + JWT auth + **email verification**
- PostgreSQL (users, samples, results, **verification tokens**)
- Redis (caching + **rate limiting**)
- **Rate limiting** (brute force/DoS protection)
- **Email verification** (token-based validation)
- **Sentry integration** (error tracking)
- **Sample types** (flour, spice, herb, other)
- Mock authenticity analysis
- **Comprehensive CI/CD** (unit + integration tests)

### Updates from Clarifications:
1. **Rate Limiting**: Redis-based protection (5 login/min, 10 upload/hour, 100 req/min)
2. **Email Verification**: Token-based before login access
3. **Sentry**: Environment-based error tracking
4. **Sample Types**: Multi-industry support
5. **CI Tests**: Both unit AND integration tests

**Impact**: 38→56 requirements (+18), 3→4 entities, 2-3→3-4 weeks

## Technical Context

**Language**: Python 3.11+
**Key Dependencies**: 
- FastAPI 0.104+, Uvicorn 0.24+, SQLAlchemy 2.0+, Pydantic 2.0+
- psycopg2-binary 2.9+, asyncpg 0.29+
- python-jose[cryptography] 3.3+, passlib[bcrypt] 1.7+
- redis 5.0+
- **slowapi 0.1.9+** (rate limiting) **[NEW]**
- **sentry-sdk[fastapi] 1.40+** (error tracking) **[NEW]**
- **aiosmtplib 3.0+** or **sendgrid 6.11+** (email) **[NEW]**
- **itsdangerous 2.1+** (token generation) **[NEW]**
- alembic 1.12+, pytest 7.4+, httpx

**Storage**: PostgreSQL 15+ + Redis 7+
**Performance**: <2s auth, <5s upload, 50 concurrent registrations, 100 concurrent requests
**Scope**: 4 entities, 7 endpoints, ~3000-4000 lines Python, 3-4 weeks

## Constitution Check ✅ PASSED

All principles satisfied with enhancements:
- ✅ Security-First: JWT + **email verification** + **rate limiting** + bcrypt + input validation
- ✅ Zero-Cost: Free tiers (**SendGrid**, **Sentry**)
- ✅ TDD: **Unit + integration tests in CI**
- ✅ Observability: Logging + **Sentry** + health checks
- ✅ Data Integrity: **Sample types** + model versioning
- ✅ API-First: REST + OpenAPI + **rate limit headers**

## Updated Database Schema

### 1. User (UPDATED):
- Added: `email_verified BOOLEAN DEFAULT FALSE`

### 2. EmailVerificationToken (NEW):
```sql
CREATE TABLE email_verification_tokens (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    token VARCHAR(255) UNIQUE,
    expires_at TIMESTAMP,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. Sample (UPDATED):
- Added: `sample_type VARCHAR(50) CHECK (sample_type IN ('flour','spice','herb','other'))`

### 4. Result (unchanged)

## Updated API Endpoints

**New**:
- GET `/auth/verify-email?token=xxx` - Verify email

**Updated**:
- POST `/auth/register` - Now sends verification email
- POST `/auth/login` - Now checks email_verified
- POST `/samples/upload` - Now requires sample_type parameter

**All endpoints**: Rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)

## New Environment Variables

```bash
# Email (choose one)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
# OR
SENDGRID_API_KEY=SG.xxx

FROM_EMAIL=noreply@instantintegrity.com
VERIFICATION_TOKEN_EXPIRY_HOURS=24

# Rate Limiting
RATE_LIMIT_ENABLED=true

# Sentry (optional)
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=development
```

## Implementation Phases (Updated)

### Phase 0: Setup (2-3 days)
- Docker + docker-compose
- **Email service config** [NEW]
- **Sentry config** [NEW]
- **Rate limiting config** [NEW]
- Database + Redis
- CI/CD skeleton

### Phase 1: Database & Models (3-4 days)
- User model + `email_verified` [UPDATED]
- **EmailVerificationToken model** [NEW]
- Sample model + `sample_type` [UPDATED]
- Result model
- Migrations with all tables
- Model tests

### Phase 2: Core Security (4-5 days)
- Password hashing
- JWT generation/validation
- **Email token generation** [NEW]
- **Email sending service** [NEW]
- **Rate limiting middleware** [NEW]
- Security tests

### Phase 3: Auth Endpoints (4-5 days)
- Register + email sending [UPDATED]
- **Verify email endpoint** [NEW]
- Login + verification check [UPDATED]
- **Rate limiting on auth** [NEW]
- Auth integration tests
- **Email workflow tests** [NEW]

### Phase 4: Sample & Analysis (3-4 days)
- CSV parser
- Mock analysis
- Upload + `sample_type` [UPDATED]
- **Sample type validation** [NEW]
- Get results
- **Rate limiting on upload** [NEW]
- Upload tests

### Phase 5: Observability (2-3 days)
- **Sentry SDK integration** [NEW]
- **Global error handler** [NEW]
- Structured logging
- Health check
- **Request context in errors** [NEW]

### Phase 6: Testing & Docs (3-4 days)
- Unit tests (80%+)
- **Integration tests** [ENHANCED]
- **Rate limiting tests** [NEW]
- **Email tests** [NEW]
- **CI: unit + integration** [UPDATED]
- Documentation updates

**Total**: 21-28 days (3-4 weeks)
**Original**: 14-21 days (2-3 weeks)
**Increase**: +7 days for production-ready features

## Updated Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── rate_limit.py [NEW]
│   │   └── email.py [NEW]
│   ├── models/
│   │   └── email_token.py [NEW]
│   ├── middleware/ [NEW]
│   │   ├── rate_limiter.py
│   │   └── error_handler.py
│   └── services/
│       └── email_service.py [NEW]
├── tests/
│   ├── unit/
│   │   ├── test_email_tokens.py [NEW]
│   │   └── test_rate_limiting.py [NEW]
│   └── integration/
│       └── test_rate_limits.py [NEW]
```

## Success Criteria (Updated)

✅ All original criteria PLUS:
- Email verification tokens expire in 24 hours
- Rate limits enforced (5 login/min, 10 upload/hour, 100 req/min)
- Sentry captures exceptions when enabled
- Sample types validated
- CI completes in <15 minutes
- Both unit + integration tests pass

## Next Steps

Ready for task breakdown: `/speckit.tasks`

Tasks will include:
- Email verification implementation
- Rate limiting middleware
- Sentry integration
- Sample type validation
- Enhanced CI configuration
- All 56 functional requirements

---

**Phase 1 Plan Updated** - Aligned with clarified specification
