<!--
  SYNC IMPACT REPORT
  Version Change: [NEW] → 1.0.0
  Modified Principles: Initial creation of all principles
  Added Sections: All core principles, security, technical standards, development workflow
  Templates Requiring Updates: All templates should align with these principles
  Follow-up TODOs: None - all principles defined
-->

# Instant Integrity MVP Constitution

## Core Principles

### I. Security-First Development (NON-NEGOTIABLE)
Security MUST be embedded from the start, not retrofitted. Every component MUST implement:
- JWT authentication on all protected endpoints
- Bcrypt password hashing for user credentials
- Input validation using Pydantic schemas
- No hardcoded secrets; environment variables only
- Minimal privilege principle for database access
- Audit trails for all sample analysis and user actions

**Rationale**: Preserving data integrity and user trust is fundamental to authenticity verification. Any security breach undermines the platform's core value proposition.

### II. Phased Delivery & Iterative Development
Development MUST follow the defined 4-phase approach:
- Phase 1: Backend skeleton with authentication and mock endpoints
- Phase 2: Chemometric model integration with real analysis
- Phase 3: Frontend development and workflow integration
- Phase 4: Scaling, observability, and performance optimization

Each phase MUST deliver working, demonstrable functionality before proceeding. No phase can be marked complete without passing all acceptance criteria.

**Rationale**: Phased delivery enables early validation, manageable scope, and allows pivoting based on feedback without large sunk costs.

### III. Zero-Cost Development & Resource Efficiency
All development MUST leverage free-tier services and open-source tools:
- Docker and docker-compose for local development
- PostgreSQL, Redis, FastAPI (all open-source)
- GitHub Actions for CI/CD (free tier)
- Optional deployment to Heroku/Render free tier
- No paid services until production deployment is justified

**Rationale**: Demonstrates technical capability while maintaining fiscal responsibility. Proves scalability roadmap before requiring investment.

### IV. Data Integrity & Scientific Rigor
All chemometric processing and AI decisions MUST be:
- Based on validated scientific methods (PCA, baseline correction, normalization)
- Transparent with confidence scores and decision thresholds
- Versioned with model metadata (training date, version, data summary)
- Reproducible with documented preprocessing pipelines
- Clear about uncertainty with "verify" status for borderline cases

**Rationale**: Authenticity verification requires scientific credibility. Opaque "black box" decisions undermine trust and regulatory compliance.

### V. Test-Driven Development
Testing MUST precede implementation:
- Unit tests for authentication, sample processing, and preprocessing
- Integration tests for API endpoints and database operations
- CI pipeline MUST pass before merging to main
- Test coverage for critical paths (auth, upload, analysis)
- Mock data and fixtures for consistent testing

**Rationale**: TDD ensures code quality, enables refactoring confidence, and documents expected behavior.

### VI. API-First Design
All functionality MUST be exposed through well-defined REST APIs:
- Clear endpoint contracts using Pydantic schemas
- Consistent response formats (status, confidence, metadata)
- Versioned endpoints to support backward compatibility
- Comprehensive API documentation (auto-generated via FastAPI)
- Stateless design for horizontal scalability

**Rationale**: API-first enables multiple frontend options, third-party integrations, and future mobile/device SDKs.

### VII. Observability & Transparency
System behavior MUST be observable at all stages:
- Structured logging at appropriate levels (INFO for operations, ERROR for failures)
- Optional Sentry integration for error tracking
- Request/response logging for API debugging
- Model inference tracking (input features, output confidence, decision)
- Performance metrics (preprocessing time, inference time, upload counts)

**Rationale**: Observability enables debugging, performance optimization, and builds confidence in system reliability.

## Security Requirements

### Authentication & Authorization
- JWT tokens MUST expire within reasonable timeframe (default 60 minutes)
- Passwords MUST meet minimum complexity requirements
- Role-based access control (operator, manager, admin) for Phase 3+
- CORS restricted to known frontend origins

### Data Protection
- No sensitive spectral data sent to external AI assistants
- Database credentials in environment variables only
- Principle of least privilege for all service accounts
- TLS/HTTPS for all production deployments

### External AI Assistant Policy
AI assistants (MCP servers) MAY be used for:
- Boilerplate code generation (controllers, schemas, utilities)
- Documentation writing and formatting
- Unit test template generation
- Code refactoring suggestions

AI assistants MUST NOT receive:
- Sample spectral data
- Model artifacts or weights
- User credentials or tokens
- Proprietary preprocessing algorithms

**All AI-generated code MUST be reviewed by human developers before commit.**

## Technical Standards

### Technology Stack (NON-NEGOTIABLE)
- Backend: Python 3.11+, FastAPI, Uvicorn
- Database: PostgreSQL 15+
- Cache: Redis 7+
- ML/Science: NumPy, SciPy, scikit-learn, matplotlib
- Security: python-jose, passlib
- Containerization: Docker, docker-compose

### Code Quality
- Type hints required for all Python functions
- Pydantic schemas for all API inputs/outputs
- SQLAlchemy models for database entities
- Maximum function complexity (avoid deeply nested logic)
- Clear separation: routes → services → models

### Database Design
- UUID primary keys for all entities
- Created_at timestamps on all tables
- Foreign key relationships properly defined
- JSON fields only for truly unstructured data
- Alembic migrations for all schema changes

## Development Workflow

### Branching Strategy
- `main`: stable, reviewed, production-ready code
- `dev`: integration branch for completed features
- `feature/*`: per-task branches linked to GitHub issues

### Pull Request Requirements
- PR MUST reference a GitHub issue
- CI tests MUST pass
- Code review required before merge to `dev`
- Description MUST explain changes and testing approach

### Issue Management
- All work MUST have a GitHub issue
- Issues MUST use appropriate labels (backend, frontend, security, phase1, etc.)
- Issues grouped by milestones (Phase 1, Phase 2, Phase 3, Phase 4)
- Clear acceptance criteria in issue description

### Commit Standards
- Conventional commit format: `type(scope): description`
- Types: feat, fix, docs, test, refactor, chore
- Reference issue number in commit message

## Model Development Standards (Phase 2+)

### Preprocessing Pipeline
- Baseline correction using validated algorithms (polynomial fitting or ALS)
- Savitzky-Golay filter for noise reduction
- Standard Normal Variate (SNV) for scatter correction
- Documented wavelength ranges for spectral windowing

### Feature Extraction
- PCA fitted on training set with variance threshold (95%)
- Separate PCA models saved as versioned artifacts
- Transform pipeline preserved for inference consistency

### Classifier Development
- One-class SVM for outlier detection on authentic samples
- Logistic regression or Random Forest when labeled adulterated samples exist
- Confidence thresholds calibrated on validation set
- Three decision classes: Authentic, Suspect, Verify

### Model Versioning
- Models saved as joblib files with semantic versioning
- Metadata includes: version, training date, training data summary, performance metrics
- Model artifacts stored in `/models` directory
- Results table includes model_version field for traceability

## Governance

### Constitution Authority
This constitution supersedes all other development practices. All team members MUST adhere to these principles.

### Amendment Process
Constitution amendments MUST:
1. Be proposed via GitHub issue with rationale
2. Be discussed and approved by project lead
3. Include version bump following semantic versioning:
   - MAJOR: Breaking changes to core principles
   - MINOR: New principles or substantial expansions
   - PATCH: Clarifications and non-semantic refinements
4. Update all dependent templates and documentation
5. Include migration plan for existing code if applicable

### Compliance Review
- All PRs MUST demonstrate compliance with applicable principles
- Violations MUST be documented and justified or corrected
- Technical debt MUST be tracked as GitHub issues
- Quarterly constitution review for relevance and completeness

### Runtime Guidance
For detailed implementation guidance, refer to:
- `README.md` for project overview and setup
- `📄 Technical Documentation – Phase 1.md` for Phase 1 specifications
- `.github/workflows/ci.yml` for CI/CD pipeline
- Individual component READMEs in `backend/app/` subdirectories

**Version**: 1.0.0 | **Ratified**: 2025-11-23 | **Last Amended**: 2025-11-23
