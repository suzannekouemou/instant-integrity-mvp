i ww# Feature Specification: Phase 1 Backend Skeleton

**Feature Branch**: `001-phase1-backend`  
**Created**: 2025-11-23  
**Status**: Draft  
**Input**: User description: "Phase 1 Backend Skeleton: FastAPI backend with JWT authentication, PostgreSQL database, Redis cache, user registration/login, mock sample upload endpoint, and Docker containerization"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Account Creation (Priority: P1)

A new user needs to create an account to access the Instant Integrity platform for spectral data analysis. They provide their email and password to register.

**Why this priority**: Without user accounts, no authenticated access is possible. This is the foundational capability for all subsequent features and must be implemented first.

**Independent Test**: Can be fully tested by submitting registration credentials via API endpoint and verifying user record creation in database. Delivers immediate value by enabling user onboarding.

**Acceptance Scenarios**:

1. **Given** no existing account, **When** user submits valid email and password, **Then** account is created successfully and confirmation is returned
2. **Given** valid registration data, **When** user attempts registration, **Then** password is securely hashed before storage
3. **Given** an existing account with the same email, **When** user attempts registration, **Then** system rejects with "email already exists" error
4. **Given** invalid email format, **When** user attempts registration, **Then** system rejects with validation error
5. **Given** password not meeting minimum requirements, **When** user attempts registration, **Then** system rejects with specific password policy error

---

### User Story 2 - User Authentication and Session Management (Priority: P1)

A registered user needs to log in to access protected endpoints and receive a JWT token for subsequent authenticated requests.

**Why this priority**: Authentication is required immediately after registration to enable users to access any protected features. This completes the basic authentication flow.

**Independent Test**: Can be fully tested by submitting valid credentials and verifying JWT token generation and validation. Delivers immediate value by securing the platform.

**Acceptance Scenarios**:

1. **Given** valid registered credentials, **When** user submits login request, **Then** system returns valid JWT token with appropriate expiration
2. **Given** invalid credentials, **When** user attempts login, **Then** system rejects with authentication error without revealing whether email or password was wrong
3. **Given** valid JWT token, **When** user makes authenticated request, **Then** system validates token and allows access
4. **Given** expired JWT token, **When** user makes authenticated request, **Then** system rejects with token expiration error
5. **Given** malformed JWT token, **When** user makes authenticated request, **Then** system rejects with invalid token error

---

### User Story 3 - Sample Data Upload for Analysis (Priority: P2)

An authenticated user needs to upload CSV spectral data files to the platform for authenticity analysis and receive preliminary results.

**Why this priority**: This demonstrates the core value proposition of the platform. While authentication is more critical, sample upload is the first real business capability.

**Independent Test**: Can be fully tested by uploading valid CSV file through authenticated endpoint and verifying mock result generation. Delivers value by showing end-to-end data flow.

**Acceptance Scenarios**:

1. **Given** authenticated user with valid CSV file, **When** user uploads spectral data, **Then** system validates file structure and stores sample record
2. **Given** valid spectral data upload, **When** system processes file, **Then** mock authenticity result is generated with status and confidence score
3. **Given** invalid file format (not CSV), **When** user attempts upload, **Then** system rejects with file type error
4. **Given** CSV with incorrect structure, **When** user uploads file, **Then** system rejects with validation error specifying required format
5. **Given** unauthenticated request, **When** upload is attempted, **Then** system rejects with authentication required error

---

### User Story 4 - Result Retrieval (Priority: P3)

An authenticated user needs to retrieve analysis results for previously uploaded samples to review authenticity decisions.

**Why this priority**: While important for completeness, this can be deferred slightly as users can receive results immediately after upload in Story 3. Adds convenience but isn't blocking.

**Independent Test**: Can be fully tested by querying for sample results by ID and verifying result data return. Delivers value through historical data access.

**Acceptance Scenarios**:

1. **Given** authenticated user and valid sample ID, **When** user requests result, **Then** system returns complete result including status, confidence, and metadata
2. **Given** non-existent sample ID, **When** user requests result, **Then** system returns not found error
3. **Given** unauthenticated request, **When** result retrieval is attempted, **Then** system rejects with authentication required error
4. **Given** authenticated user requesting another user's sample, **When** result retrieval is attempted, **Then** system rejects with authorization error

---

### Edge Cases

- What happens when a user tries to register with an extremely long email (>320 characters)?
- How does the system handle simultaneous login attempts from the same account?
- What happens when CSV upload exceeds maximum file size limit?
- How does system handle malformed JWT tokens that decode but contain invalid claims?
- What happens when database connection is lost during registration or login?
- How does system handle CSV files with unusual encoding (UTF-16, non-English characters)?
- What happens when Redis cache is unavailable but requests are still coming in?
- How does system respond to rapid repeated login attempts (potential brute force)?

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & User Management

- **FR-001**: System MUST provide REST API endpoint for user registration accepting email and password
- **FR-002**: System MUST validate email format according to RFC 5322 standard
- **FR-003**: System MUST enforce minimum password complexity: at least 8 characters
- **FR-004**: System MUST hash passwords using bcrypt before storage, never storing plain text
- **FR-005**: System MUST prevent duplicate email registration and return appropriate error
- **FR-006**: System MUST send verification email with unique token upon user registration
- **FR-007**: System MUST store email verification token with expiration (24 hours) in database
- **FR-008**: System MUST provide endpoint to verify email via token link
- **FR-009**: System MUST mark user account as verified upon successful email verification
- **FR-010**: System MUST allow login only for users with verified email addresses
- **FR-011**: System MUST provide REST API endpoint for user login accepting email and password
- **FR-012**: System MUST generate JWT tokens upon successful authentication with configurable expiration (default 60 minutes)
- **FR-013**: System MUST include user ID and role in JWT token payload for authorization decisions
- **FR-014**: System MUST validate JWT tokens on all protected endpoints before processing requests
- **FR-015**: System MUST reject expired, malformed, or invalid JWT tokens with appropriate HTTP status codes

#### Sample Upload & Processing

- **FR-016**: System MUST provide authenticated REST API endpoint for CSV file upload
- **FR-017**: System MUST validate CSV file structure containing wavelength and absorbance columns
- **FR-018**: System MUST accept sample_type parameter with values: flour, spice, herb, other
- **FR-019**: System MUST store sample metadata including filename, sample_type, user ID, upload timestamp
- **FR-020**: System MUST persist spectral data points associated with each sample
- **FR-021**: System MUST generate mock authenticity result with status (Authentic/Suspect) and confidence score (0.80-0.95)
- **FR-022**: System MUST return result immediately after successful upload
- **FR-023**: System MUST link sample records to authenticated user for ownership tracking

#### Result Management

- **FR-024**: System MUST provide authenticated REST API endpoint to retrieve results by sample ID
- **FR-025**: System MUST return result including status, confidence, model version, sample_type, and summary
- **FR-026**: System MUST enforce authorization ensuring users can only access their own samples
- **FR-027**: System MUST persist results with sample ID, timestamps, and model version metadata

#### Data Persistence & Caching

- **FR-028**: System MUST persist users in PostgreSQL with UUID primary keys, email_verified boolean, and created_at timestamps
- **FR-029**: System MUST persist email verification tokens with token string, expiration timestamp, and user foreign key
- **FR-030**: System MUST persist samples in PostgreSQL with UUID primary keys, sample_type enum, user foreign keys, and metadata
- **FR-031**: System MUST persist results in PostgreSQL with UUID primary keys and sample foreign keys
- **FR-032**: System MUST connect to Redis for caching and rate limiting
- **FR-033**: System MUST use environment variables for all database connection strings and secrets
- **FR-034**: System MUST implement proper database connection pooling and error handling

#### Infrastructure & Deployment

- **FR-035**: System MUST be containerized using Docker with Dockerfile for FastAPI application
- **FR-036**: System MUST provide docker-compose.yml orchestrating backend, PostgreSQL, and Redis services
- **FR-037**: System MUST expose backend on configurable port (default 8000)
- **FR-038**: System MUST define health check endpoint for container orchestration
- **FR-039**: System MUST log application events at appropriate levels (INFO, ERROR)
- **FR-040**: System MUST handle CORS configuration for frontend access (Phase 3 preparation)
- **FR-041**: System MUST configure email service (SMTP or API-based like SendGrid free tier)
- **FR-042**: System MUST integrate Sentry SDK for error tracking, enabled when SENTRY_DSN environment variable is provided
- **FR-043**: System MUST capture and report unhandled exceptions to Sentry when enabled
- **FR-044**: System MUST include request context (user ID, endpoint, method) in Sentry error reports

#### Security & Rate Limiting

- **FR-045**: System MUST implement rate limiting on authentication endpoints: maximum 5 login attempts per minute per IP address
- **FR-046**: System MUST implement rate limiting on registration endpoint: maximum 3 registrations per hour per IP address
- **FR-047**: System MUST implement rate limiting on upload endpoint: maximum 10 uploads per hour per authenticated user
- **FR-048**: System MUST implement general API rate limiting: maximum 100 requests per minute per authenticated user
- **FR-049**: System MUST use Redis to store rate limit counters with appropriate expiration
- **FR-050**: System MUST return HTTP 429 (Too Many Requests) with Retry-After header when rate limits exceeded

#### Input Validation & Error Handling

- **FR-051**: System MUST validate all API inputs using Pydantic schemas
- **FR-052**: System MUST return consistent error response format with status code, message, and optional details
- **FR-053**: System MUST not expose stack traces or internal errors in API responses
- **FR-054**: System MUST enforce maximum file size limit for CSV uploads (default 10MB)
- **FR-055**: System MUST sanitize file names to prevent path traversal attacks
- **FR-056**: System MUST validate sample_type parameter against allowed enum values (flour, spice, herb, other)

### Key Entities

- **User**: Represents registered platform users with email (unique identifier), password hash, email_verified boolean, optional role designation, and creation timestamp
- **Sample**: Represents uploaded spectral data with filename, sample_type (enum: flour/spice/herb/other), spectra points (array/JSON), metadata (device type, location, timestamp), and ownership link to User
- **Result**: Represents analysis outcomes with status (Authentic/Suspect/Verify), confidence score (float 0-1), model version identifier, summary text, and link to Sample
- **EmailVerificationToken**: Represents email verification tokens with token string, expiration timestamp, used boolean, and link to User

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration in under 30 seconds from API call to confirmation
- **SC-002**: Users can complete login and receive JWT token in under 2 seconds
- **SC-003**: CSV file upload and mock result generation completes in under 5 seconds for files up to 10MB
- **SC-004**: System handles 50 concurrent user registrations without failures or timeouts
- **SC-005**: System handles 100 concurrent authenticated requests without degradation
- **SC-006**: Invalid authentication attempts return appropriate errors within 1 second without revealing security details
- **SC-007**: Docker containers start successfully on first run with docker-compose up command
- **SC-008**: All API endpoints return responses with appropriate HTTP status codes (200, 201, 400, 401, 404, 500)
- **SC-009**: Database schema supports future expansion with proper foreign key relationships and indexing strategy
- **SC-010**: Zero plain-text passwords or secrets committed to version control or visible in logs

## Assumptions

1. **Email as unique identifier**: We assume email is sufficient for user identification in Phase 1; additional profile fields can be added later
2. **Single-role system**: All users have same permissions in Phase 1; role-based access control deferred to Phase 3
3. **Mock analysis only**: Phase 1 uses placeholder logic for authenticity determination; real chemometric models added in Phase 2
4. **Local development focus**: Primary deployment target is local docker-compose; cloud deployment (Heroku/Render) is optional demonstration
5. **Spectral data format**: CSV format is wavelength-absorbance pairs; more complex formats (vendor-specific) handled in future phases
6. **File storage**: Spectral data stored in database JSON field for Phase 1; separate file storage (S3) considered for Phase 2+
7. **No password reset**: Password reset functionality deferred to Phase 2; Phase 1 focuses on core authentication
8. **English-only errors**: Error messages and validation in English; internationalization deferred to Phase 3+
9. **Standard web application threat model**: No advanced security features (rate limiting, intrusion detection) in Phase 1; focus on foundational security (JWT, bcrypt, input validation)

## Dependencies

- **External dependencies**: None - fully self-contained Phase 1 deployment
- **Internal dependencies**: Must complete constitution review before implementation begins (currently on dev branch)
- **Team dependencies**: Single developer workflow; code review can be self-review for Phase 1
- **Technical dependencies**: Requires Docker and docker-compose on development machine; no cloud services required

## Out of Scope

The following are explicitly **not** included in Phase 1:

- Real chemometric preprocessing or machine learning models
- Batch processing of multiple samples
- Advanced visualization or dashboard UI
- Password reset flows (requires verified email from Phase 1)
- User profile management beyond basic registration
- Sample sharing between users
- Export functionality (CSV/PDF reports)
- Mobile application or device SDK integration
- Advanced monitoring (Prometheus, Grafana)
- Frontend application (Next.js) - Phase 3
- Role-based access control - Phase 3
- Cloud deployment beyond optional demo - Phase 4
- Advanced rate limiting features (IP blocking, exponential backoff, distributed rate limiting) - Phase 2
- Advanced email features (email templates, transactional email tracking, bounce handling) - Phase 2
- Advanced Sentry features (performance monitoring, custom tags, release tracking) - Phase 2

## Notes

- **Testing strategy**: Phase 1 requires comprehensive unit tests for authentication, security functions, and business logic, plus integration tests for all API endpoints. Both test suites MUST run in CI pipeline before merge to dev.
- **CI/CD pipeline**: GitHub Actions MUST run unit tests, integration tests (with test database), linting, and Docker build on all PRs to dev and main branches.
- **Documentation priority**: Code should be well-commented; API documentation auto-generated via FastAPI's built-in Swagger UI
- **Migration strategy**: Use Alembic for database migrations from the start to enable clean schema evolution
- **Security review**: JWT secret must be strong random value in production; document environment variable requirements clearly
- **Email service**: Use free-tier email service (SendGrid, AWS SES sandbox, or SMTP) for Phase 1; production email service in Phase 4
- **Performance baseline**: Establish baseline metrics in Phase 1 (response times, concurrent users) for comparison in later phases

## Clarifications

### Session 2025-11-23
- Q: Should Phase 1 include API integration tests in CI pipeline or just unit tests? → A: Yes, both unit and integration tests - Complete coverage, ~5-10 min CI time, catches all issues
- Q: Should the system support multiple sample types (e.g., flour, spices, herbs) with type-specific validation in Phase 1, or treat all samples uniformly? → A: Yes, add basic sample types - Add sample_type enum field (flour, spice, herb, other), store in metadata
- Q: Should basic Sentry integration be included in Phase 1 for error tracking and debugging, or keep it fully optional? → A: Yes, implement with env flag - Sentry SDK integrated, enabled only when SENTRY_DSN provided
- Q: Should email verification be included in Phase 1 to ensure users provide valid email addresses and prevent fake account creation? → A: Yes, add basic email verification - Send verification link, require verification before full access

- Q: Should basic rate limiting and abuse prevention be included in Phase 1 to protect authentication endpoints from brute force attacks and upload endpoint from resource exhaustion? → A: Yes, add basic rate limiting - Simple Redis-based limits: 5 login attempts/min, 10 uploads/hour per user, 100 API calls/min
