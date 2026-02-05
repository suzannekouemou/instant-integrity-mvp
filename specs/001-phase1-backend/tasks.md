# Implementation Tasks: Phase 1 Backend Skeleton

**Feature Branch**: `001-phase1-backend`  
**Created**: 2025-11-23  
**Specification**: [spec.md](./spec.md)  
**Implementation Plan**: [plan.md](./plan.md)

## Overview

This document breaks down Phase 1 Backend implementation into granular, executable tasks organized by user story. Each task is designed to be completable in 2-4 hours.

**Total Estimated Effort**: 21-28 days (3-4 weeks)
**Total Tasks**: 87 tasks
**Parallel Opportunities**: 42 parallelizable tasks marked with [P]

## Task Organization

Tasks are organized into phases:
1. **Setup** - Project initialization and infrastructure
2. **Foundational** - Core components needed by all user stories
3. **User Story 1 (P1)** - User Registration + Email Verification
4. **User Story 2 (P1)** - Authentication & Session Management
5. **User Story 3 (P2)** - Sample Upload & Mock Analysis
6. **User Story 4 (P3)** - Result Retrieval
7. **Polish** - Cross-cutting concerns and finalization

## Phase 1: Setup & Infrastructure (2-3 days)

**Goal**: Initialize project structure, Docker environment, and foundational configuration

### Setup Tasks

- [x] T001 Create backend directory structure per plan.md (app/, tests/, alembic/) ✓ Completed 2025-11-24
- [x] T002 [P] Create requirements.txt with all dependencies from plan.md ✓ Completed 2025-11-24 (backend/requirements.txt)
- [x] T003 [P] Create .env.example with all required environment variables ✓ Completed 2025-11-24 (backend/.env.example)
- [x] T004 [P] Create Dockerfile for FastAPI application ✓ Completed 2025-11-24 (backend/Dockerfile)
- [x] T005 Create docker-compose.yml orchestrating backend, PostgreSQL, Redis services ✓ Completed 2025-11-24 (docker-compose.yml)
- [x] T006 [P] Create .gitignore for Python project (venv/, __pycache__/, .env, etc.) ✓ Completed 2025-11-24 (pre‑existing, verified)
- [x] T007 Initialize Alembic in backend/ directory with alembic init alembic ✓ Completed 2025-11-24 (backend/alembic/*)
- [x] T008 [P] Configure alembic.ini with DATABASE_URL from environment ✓ Completed 2025-11-24 (backend/alembic.ini)
- [x] T009 [P] Update alembic/env.py to import models and use async engine ✓ Completed 2025-11-24 (backend/alembic/env.py)
- [x] T010 [P] Create pytest.ini with test configuration and coverage settings ✓ Completed 2025-11-24 (backend/pytest.ini)
- [x] T011 [P] Create tests/conftest.py with database and client fixtures ✓ Completed 2025-11-24 (backend/tests/conftest.py)
- [x] T012 Create GitHub Actions workflow .github/workflows/ci.yml with unit + integration tests ✓ Completed 2025-11-24 (.github/workflows/ci.yml)

**Acceptance**: Docker containers start successfully, database accessible, Alembic ready

---

## Phase 2: Foundational Components (4-5 days)

**Goal**: Implement core utilities, models, and middleware needed by all user stories

### Configuration & Core Setup

- [x] T013 Create app/core/config.py with Pydantic Settings for all environment variables ✓ Completed 2025-11-24 (backend/app/core/config.py)
- [x] T014 [P] Create app/core/database.py with async SQLAlchemy engine and session management ✓ Completed 2025-11-24 (backend/app/core/database.py)
- [x] T015 [P] Create app/core/security.py with password hashing (bcrypt) and JWT functions ✓ Completed 2025-11-24 (backend/app/core/security.py)
- [x] T016 [P] Create app/core/email.py with email configuration (SMTP/SendGrid) ✓ Completed 2025-11-24 (backend/app/core/email.py)
- [x] T017 [P] Create app/core/rate_limit.py with rate limiting configuration and decorators ✓ Completed 2025-11-24 (backend/app/core/rate_limit.py)
- [x] T018 Create app/main.py with FastAPI app initialization, CORS, and Sentry integration ✓ Completed 2025-11-24 (backend/app/main.py)

### Database Models

- [x] T019 [P] Create app/models/__init__.py with Base model import ✓ Completed 2025-11-24
- [x] T020 [P] Create app/models/user.py with User model (email, password_hash, email_verified, role) ✓ Completed 2025-11-24
- [x] T021 [P] Create app/models/email_token.py with EmailVerificationToken model ✓ Completed 2025-11-24
- [x] T022 [P] Create app/models/sample.py with Sample model (filename, sample_type, spectra_points, metadata) ✓ Completed 2025-11-24
- [x] T023 [P] Create app/models/result.py with Result model (status, confidence, model_version, summary) ✓ Completed 2025-11-24
- [x] T024 Create initial Alembic migration alembic/versions/001_initial_schema.py for all tables ✓ Completed 2025-11-24

### Middleware & Error Handling

- [x] T025 Create app/middleware/__init__.py ✓ Completed 2025-11-24
- [x] T026 [P] Create app/middleware/rate_limiter.py with slowapi integration for rate limiting ✓ Completed 2025-11-24
- [x] T027 [P] Create app/middleware/error_handler.py with global exception handler and Sentry ✓ Completed 2025-11-24

### Services & Utilities

- [x] T028 Create app/services/__init__.py ✓ Completed 2025-11-24
- [x] T029 [P] Create app/utils/__init__.py ✓ Completed 2025-11-24
- [x] T030 [P] Create app/utils/tokens.py with secure token generation using itsdangerous ✓ Completed 2025-11-24

**Acceptance**: All models defined, migrations run, middleware configured, utilities available

---

## Phase 3: User Story 1 - Registration & Email Verification (4-5 days)

**User Story**: User Registration and Account Creation (Priority P1)

**Goal**: Users can register with email/password, receive verification email, and verify their account

**Independent Test**: Submit registration → verify email sent → verify token → confirm email_verified=true in DB

### Pydantic Schemas

- [x] T031 [P] [US1] Create app/schemas/__init__.py ✓ Completed 2025-11-24
- [x] T032 [P] [US1] Create app/schemas/auth.py with UserCreate, UserResponse, Token, EmailVerify schemas ✓ Completed 2025-11-24

### Email Service

- [x] T033 [US1] Create app/services/email_service.py with send_verification_email function ✓ Completed 2025-11-24
- [x] T034 [US1] Create HTML email template for verification link ✓ Completed 2025-11-24
- [x] T035 [P] [US1] Add email service unit tests in tests/unit/test_email_service.py ✓ Completed 2025-11-24

### Authentication Service

- [x] T036 [US1] Create app/services/auth_service.py with create_user function (hash password, create token, send email) ✓ Completed 2025-11-24
- [x] T037 [US1] Add verify_email function in auth_service.py (validate token, mark user verified) ✓ Completed 2025-11-24
- [x] T038 [P] [US1] Add unit tests for auth_service in tests/unit/test_auth_service.py ✓ Completed 2025-11-24

### API Endpoints

- [x] T039 Create app/routes/__init__.py ✓ Completed 2025-11-24
- [x] T040 [US1] Create app/routes/auth.py with POST /auth/register endpoint (rate limited: 3/hour per IP) ✓ Completed 2025-11-24
- [x] T041 [US1] Add GET /auth/verify-email?token=xxx endpoint in app/routes/auth.py ✓ Completed 2025-11-24
- [x] T042 [US1] Register auth router in app/main.py under /api/v1/auth ✓ Completed 2025-11-24

### Integration Tests

- [x] T043 [US1] Create tests/integration/test_registration.py testing full registration flow ✓ Completed 2025-11-24
- [x] T044 [US1] Add email verification flow tests in tests/integration/test_registration.py ✓ Completed 2025-11-24
- [x] T045 [US1] Add rate limiting tests for registration in tests/integration/test_rate_limits.py ✓ Completed 2025-11-24

**US1 Acceptance Criteria**:
- ✓ User can register with valid email/password
- ✓ Verification email sent with valid token
- ✓ Token expires after 24 hours
- ✓ Email verification endpoint validates token
- ✓ User marked as email_verified=true after verification
- ✓ Rate limit enforced (3 registrations/hour per IP)

---

## Phase 4: User Story 2 - Authentication & Login (4-5 days)

**User Story**: User Authentication and Session Management (Priority P1)

**Goal**: Verified users can log in with credentials and receive JWT token for authenticated requests

**Independent Test**: Register → verify email → login → receive JWT → use token on protected endpoint

**Dependencies**: Requires US1 (user registration and email verification)

### Authentication Logic

- [x] T046 [US2] Add authenticate_user function in app/services/auth_service.py (check email_verified, verify password) ✓ Completed 2025-11-24
- [x] T047 [US2] Add create_access_token function in app/core/security.py (generate JWT with user_id, role, expiration) ✓ Completed 2025-11-24
- [x] T048 [P] [US2] Add unit tests for JWT creation/validation in tests/unit/test_security.py ✓ Completed 2025-11-24

### JWT Dependency

- [x] T049 [US2] Create app/core/dependencies.py with get_current_user dependency (validate JWT, extract user) ✓ Completed 2025-11-24
- [x] T050 [P] [US2] Add unit tests for JWT dependency in tests/unit/test_dependencies.py ✓ Completed 2025-11-24

### Login Endpoint

- [x] T051 [US2] Add POST /auth/login endpoint in app/routes/auth.py (rate limited: 5/min per IP) ✓ Completed 2025-11-24
- [x] T052 [US2] Add email verification check in login endpoint (return 403 if not verified) ✓ Completed 2025-11-24
- [x] T053 [P] [US2] Add Pydantic LoginRequest schema in app/schemas/auth.py ✓ Completed 2025-11-24

### Integration Tests

- [x] T054 [US2] Create tests/integration/test_login.py testing successful login flow ✓ Completed 2025-11-24
- [x] T055 [US2] Add unverified email rejection test in tests/integration/test_login.py ✓ Completed 2025-11-24
- [x] T056 [US2] Add invalid credentials test in tests/integration/test_login.py ✓ Completed 2025-11-24
- [x] T057 [US2] Add JWT token validation tests in tests/integration/test_login.py ✓ Completed 2025-11-24
- [x] T058 [US2] Add rate limiting tests for login in tests/integration/test_rate_limits.py ✓ Completed 2025-11-24

**US2 Acceptance Criteria**:
- ✓ Verified users can log in with correct credentials
- ✓ Unverified users receive 403 Forbidden
- ✓ Invalid credentials return 401 Unauthorized
- ✓ JWT token generated with 60-minute expiration
- ✓ JWT includes user_id and role in payload
- ✓ Protected endpoints validate JWT correctly
- ✓ Rate limit enforced (5 login attempts/min per IP)

---

## Phase 5: User Story 3 - Sample Upload & Analysis (3-4 days)

**User Story**: Sample Data Upload for Analysis (Priority P2)

**Goal**: Authenticated users upload CSV spectral data and receive mock authenticity results

**Independent Test**: Login → upload CSV with sample_type → verify sample stored → verify mock result returned

**Dependencies**: Requires US2 (authentication for JWT token)

### CSV Parser & Validation

- [x] T059 [P] [US3] Create app/utils/csv_parser.py with validate_csv function (check columns, data types, wavelength range) ✓ Completed 2025-11-24
- [x] T060 [P] [US3] Add unit tests for CSV parser in tests/unit/test_csv_parser.py ✓ Completed 2025-11-24
- [x] T061 [P] [US3] Create sample CSV test files in tests/fixtures/ (valid and invalid) ✓ Completed 2025-11-24

### Mock Analysis Service

- [x] T062 [P] [US3] Create app/services/analysis_service.py with generate_mock_result function ✓ Completed 2025-11-24
- [x] T063 [P] [US3] Add unit tests for mock analysis in tests/unit/test_analysis_service.py ✓ Completed 2025-11-24

### Pydantic Schemas

- [x] T064 [P] [US3] Create app/schemas/sample.py with SampleUpload, SampleResponse, SampleType enum schemas ✓ Completed 2025-11-24
- [x] T065 [P] [US3] Create app/schemas/result.py with ResultResponse schema ✓ Completed 2025-11-24

### Upload Endpoint

- [x] T066 [US3] Create app/routes/samples.py with POST /samples/upload endpoint (requires auth, rate limited: 10/hour per user) ✓ Completed 2025-11-24
- [x] T067 [US3] Add sample_type validation in upload endpoint (enum: flour, spice, herb, other) ✓ Completed 2025-11-24
- [x] T068 [US3] Add file size validation (max 10MB) in upload endpoint ✓ Completed 2025-11-24
- [x] T069 [US3] Add CSV parsing and storage logic in upload endpoint ✓ Completed 2025-11-24
- [x] T070 [US3] Add mock result generation and return in upload endpoint ✓ Completed 2025-11-24
- [x] T071 [US3] Register samples router in app/main.py under /api/v1/samples ✓ Completed 2025-11-24

### Integration Tests

- [x] T072 [US3] Create tests/integration/test_sample_upload.py with valid upload test ✓ Completed 2025-11-24
- [x] T073 [US3] Add invalid CSV format test in tests/integration/test_sample_upload.py ✓ Completed 2025-11-24
- [x] T074 [US3] Add sample_type validation tests in tests/integration/test_sample_upload.py ✓ Completed 2025-11-24
- [x] T075 [US3] Add file size limit test in tests/integration/test_sample_upload.py ✓ Completed 2025-11-24
- [x] T076 [US3] Add unauthenticated upload rejection test in tests/integration/test_sample_upload.py ✓ Completed 2025-11-24
- [x] T077 [US3] Add rate limiting tests for upload in tests/integration/test_rate_limits.py ✓ Completed 2025-11-24

**US3 Acceptance Criteria**:
- ✓ Authenticated users can upload valid CSV files
- ✓ Sample_type parameter required (flour, spice, herb, other)
- ✓ CSV structure validated (wavelength, absorbance columns)
- ✓ File size limit enforced (10MB)
- ✓ Sample stored with spectral data and metadata
- ✓ Mock result generated and returned immediately
- ✓ Unauthenticated requests rejected
- ✓ Rate limit enforced (10 uploads/hour per user)

---

## Phase 6: User Story 4 - Result Retrieval (2-3 days)

**User Story**: Result Retrieval (Priority P3)

**Goal**: Authenticated users retrieve analysis results for previously uploaded samples

**Independent Test**: Login → upload sample → get sample_id → retrieve result → verify result data

**Dependencies**: Requires US2 (authentication), US3 (samples exist)

### Result Retrieval Endpoint

- [x] T078 [US4] Create app/routes/results.py with GET /results/{sample_id} endpoint (requires auth) ✓ Completed 2025-11-24
- [x] T079 [US4] Add authorization check in results endpoint (user can only access own samples) ✓ Completed 2025-11-24
- [x] T080 [US4] Add 404 handling for non-existent sample IDs ✓ Completed 2025-11-24
- [x] T081 [US4] Register results router in app/main.py under /api/v1/results ✓ Completed 2025-11-24

### Integration Tests

- [x] T082 [US4] Create tests/integration/test_result_retrieval.py with successful retrieval test ✓ Completed 2025-11-24
- [x] T083 [US4] Add non-existent sample test in tests/integration/test_result_retrieval.py ✓ Completed 2025-11-24
- [x] T084 [US4] Add authorization test (user B cannot access user A's samples) in tests/integration/test_result_retrieval.py ✓ Completed 2025-11-24
- [x] T085 [US4] Add unauthenticated request test in tests/integration/test_result_retrieval.py ✓ Completed 2025-11-24

**US4 Acceptance Criteria**:
- ✓ Authenticated users can retrieve results by sample_id
- ✓ Result includes status, confidence, model_version, sample_type, summary
- ✓ Users can only access their own samples (authorization enforced)
- ✓ Non-existent sample_id returns 404
- ✓ Unauthenticated requests rejected

---

## Phase 7: Polish & Cross-Cutting Concerns (2-3 days)

**Goal**: Add health check, finalize documentation, ensure all tests pass

### Health & Monitoring

- [x] T086 Create GET /health endpoint in app/main.py (check database and Redis connections) ✓ Completed 2025-11-24
- [x] T087 Add rate limit headers (slowapi handles automatically) ✓ Completed 2025-11-24

### Testing & Documentation

- [x] T088 Run full test suite and verify 80%+ code coverage ✓ Completed 2025-11-24
- [x] T089 Update README.md with setup instructions and API documentation links ✓ Completed 2025-11-24
- [x] T090 Update .env.example with all new environment variables ✓ Completed 2025-11-24
- [x] T091 Verify CI pipeline passes all tests (unit + integration) ✓ Completed 2025-11-24
- [x] T092 Create API documentation review using FastAPI /docs endpoint ✓ Completed 2025-11-24
- [x] T093 Test Docker compose up workflow end-to-end ✓ Completed 2025-11-24

**Final Acceptance**: All 56 requirements implemented, tests passing, Docker working, CI green

---

## Task Dependencies & Parallel Execution

### Critical Path (Sequential)
1. Setup (Phase 1) → Must complete first
2. Foundational (Phase 2) → Blocks all user stories
3. US1 (Registration) → Blocks US2 (needs users)
4. US2 (Authentication) → Blocks US3, US4 (needs JWT)
5. US3 (Upload) → Independent of US4
6. US4 (Results) → Can start after US3
7. Polish (Phase 7) → Final phase

### Parallel Opportunities

**Within Foundational Phase (Phase 2)**:
- All schemas can be created in parallel (T031-T065)
- All utility functions can be created in parallel (T029-T030)
- All unit tests can be written in parallel after their targets

**Within User Story Phases**:
- Schemas, services, and utilities within a story can be developed in parallel
- Unit tests can be written alongside implementation
- Integration tests written after endpoint implementation

**Example Parallel Workflow for US3**:
```
Developer A: CSV parser + unit tests (T059, T060)
Developer B: Mock analysis service + unit tests (T062, T063)
Developer C: Schemas (T064, T065)
→ Merge all
→ Together: Upload endpoint (T066-T070)
→ Integration tests (T072-T077)
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
**Recommended**: Complete through US2 (Authentication) for MVP demo
- Demonstrates: User registration, email verification, secure login, JWT tokens
- Value: Fully secure authentication system ready for extension
- Effort: ~12-15 days

### Incremental Delivery
1. **Week 1**: Setup + Foundational + US1 (Registration)
2. **Week 2**: US2 (Authentication) + US3 start
3. **Week 3**: US3 (Upload) + US4 (Results)
4. **Week 4**: Polish, testing, documentation

### Testing Approach
- **Unit tests**: Written alongside or before implementation (TDD optional)
- **Integration tests**: Written after endpoint implementation
- **CI Pipeline**: All tests must pass before merge to dev

---

## Task Status Tracking

Update task status by checking boxes:
- `- [ ]` = Not started
- `- [x]` = Complete
- Add notes inline for blocked tasks

**Example**:
```
- [x] T001 Create backend directory structure ✓ Completed 2025-11-23
- [ ] T002 [P] Create requirements.txt (Blocked: awaiting dependency versions)
```

---

**Total Tasks**: 93
**Estimated Completion**: 21-28 days (3-4 weeks)
**Next Step**: Begin with T001 and work sequentially through Setup phase

