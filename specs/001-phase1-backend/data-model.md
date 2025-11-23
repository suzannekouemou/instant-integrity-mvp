# Phase 1: Data Model Design

**Feature**: Phase 1 Backend Skeleton  
**Date**: 2025-11-23  
**Purpose**: Define database schema, entity relationships, and validation rules

## Overview

This document defines the database schema for Phase 1 backend. The design supports:
- User authentication and ownership tracking
- Sample spectral data storage
- Mock analysis results with model versioning
- Future expansion for Phase 2+ features

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ password_hash   │
│ role            │
│ created_at      │
└────────┬────────┘
         │
         │ owns (1:N)
         │
         ▼
┌─────────────────┐
│     Sample      │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │◄────┐
│ filename        │     │
│ spectra_points  │     │ has result (1:1)
│ metadata        │     │
│ created_at      │     │
└────────┬────────┘     │
         │              │
         │              │
         ▼              │
┌─────────────────┐     │
│     Result      │     │
├─────────────────┤     │
│ id (PK)         │     │
│ sample_id (FK)  ├─────┘
│ status          │
│ confidence      │
│ model_version   │
│ summary         │
│ created_at      │
└─────────────────┘
```

---

## Entity Definitions

### 1. User Entity

**Purpose**: Registered platform users who can upload samples and access results

**Table**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique user identifier |
| `email` | VARCHAR(320) | UNIQUE, NOT NULL | User email (RFC 5322 max length) |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt-hashed password |
| `role` | VARCHAR(50) | DEFAULT 'user' | User role (user, admin - Phase 3) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

**Indexes**:
- `idx_users_email` on `email` (UNIQUE) - Fast lookup during login

**Validation Rules**:
- Email: RFC 5322 format validation
- Password: Minimum 8 characters before hashing
- Role: Enum ('user', 'admin') - enforced at application level in Phase 1

**SQLAlchemy Model**:
```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(320), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    samples = relationship("Sample", back_populates="user")
```

**Sample Data**:
```json
{
  "id": "a1b2c3d4-e5f6-4789-9012-3456789abcde",
  "email": "user@example.com",
  "password_hash": "$2b$12$...", 
  "role": "user",
  "created_at": "2025-11-23T16:40:00Z"
}
```

---

### 2. Sample Entity

**Purpose**: Uploaded spectral data files with metadata and ownership

**Table**: `samples`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique sample identifier |
| `user_id` | UUID | FOREIGN KEY REFERENCES users(id), NOT NULL | Sample owner |
| `filename` | VARCHAR(255) | NOT NULL | Original uploaded filename |
| `spectra_points` | JSONB | NOT NULL | Array of {wavelength, absorbance} objects |
| `metadata` | JSONB | DEFAULT '{}' | Device type, location, timestamp, etc. |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Upload time |

**Indexes**:
- `idx_samples_user_id` on `user_id` - Fast lookup of user's samples
- `idx_samples_created_at` on `created_at` - Chronological queries
- GIN index on `spectra_points` - JSONB query optimization (Phase 2+)

**Validation Rules**:
- Filename: Sanitized to prevent path traversal (remove ../, absolute paths)
- Spectra Points: Array of objects, each with numeric wavelength & absorbance
- Maximum 10,000 data points per sample
- Wavelength range: 200-2500 nm (configurable)

**SQLAlchemy Model**:
```python
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Sample(Base):
    __tablename__ = "samples"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    spectra_points = Column(JSONB, nullable=False)
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="samples")
    result = relationship("Result", back_populates="sample", uselist=False)
```

**Sample Data**:
```json
{
  "id": "f1e2d3c4-b5a6-4789-9012-3456789abcde",
  "user_id": "a1b2c3d4-e5f6-4789-9012-3456789abcde",
  "filename": "sample_flour_01.csv",
  "spectra_points": [
    {"wavelength": 400.0, "absorbance": 0.123},
    {"wavelength": 401.0, "absorbance": 0.125},
    ...
  ],
  "metadata": {
    "device_type": "Handheld NIR",
    "location": "Warehouse A",
    "operator": "John Doe"
  },
  "created_at": "2025-11-23T16:45:00Z"
}
```

---

### 3. Result Entity

**Purpose**: Analysis outcomes for uploaded samples (mock in Phase 1)

**Table**: `results`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique result identifier |
| `sample_id` | UUID | FOREIGN KEY REFERENCES samples(id), UNIQUE, NOT NULL | Associated sample (1:1) |
| `status` | VARCHAR(50) | NOT NULL | Analysis outcome: Authentic, Suspect, Verify |
| `confidence` | FLOAT | CHECK (confidence >= 0 AND confidence <= 1) | Confidence score 0-1 |
| `model_version` | VARCHAR(100) | NOT NULL | Model identifier (e.g., "mock-v1.0") |
| `summary` | TEXT | | Human-readable explanation |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Analysis completion time |

**Indexes**:
- `idx_results_sample_id` on `sample_id` (UNIQUE) - One result per sample
- `idx_results_status` on `status` - Filter by authenticity status
- `idx_results_created_at` on `created_at` - Chronological queries

**Validation Rules**:
- Status: Enum ('Authentic', 'Suspect', 'Verify') - enforced at application level
- Confidence: Float between 0.0 and 1.0 (database CHECK constraint)
- Model Version: Required, formatted as semantic version or identifier

**SQLAlchemy Model**:
```python
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Result(Base):
    __tablename__ = "results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sample_id = Column(UUID(as_uuid=True), ForeignKey("samples.id"), unique=True, nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)
    confidence = Column(Float, CheckConstraint('confidence >= 0 AND confidence <= 1'), nullable=False)
    model_version = Column(String(100), nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationship
    sample = relationship("Sample", back_populates="result")
```

**Sample Data**:
```json
{
  "id": "e1f2g3h4-i5j6-4789-9012-3456789abcde",
  "sample_id": "f1e2d3c4-b5a6-4789-9012-3456789abcde",
  "status": "Authentic",
  "confidence": 0.87,
  "model_version": "mock-v1.0",
  "summary": "Phase 1 mock result. Real chemometric analysis in Phase 2.",
  "created_at": "2025-11-23T16:45:01Z"
}
```

---

## Migration Strategy

### Alembic Migration Plan

**Initial Migration** (`001_initial_schema.py`):
```python
def upgrade():
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('email', sa.String(320), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), server_default='user', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    
    # Create samples table
    op.create_table(
        'samples',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('spectra_points', postgresql.JSONB, nullable=False),
        sa.Column('metadata', postgresql.JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_samples_user_id', 'samples', ['user_id'])
    op.create_index('idx_samples_created_at', 'samples', ['created_at'])
    
    # Create results table
    op.create_table(
        'results',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('sample_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('samples.id'), unique=True, nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('confidence', sa.Float, nullable=False),
        sa.Column('model_version', sa.String(100), nullable=False),
        sa.Column('summary', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_index('idx_results_sample_id', 'results', ['sample_id'], unique=True)
    op.create_index('idx_results_status', 'results', ['status'])
    op.create_index('idx_results_created_at', 'results', ['created_at'])
    
    # Add constraint for confidence range
    op.create_check_constraint(
        'ck_results_confidence_range',
        'results',
        'confidence >= 0 AND confidence <= 1'
    )

def downgrade():
    op.drop_table('results')
    op.drop_table('samples')
    op.drop_table('users')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
```

### Future Migration Considerations (Phase 2+)

- **Phase 2**: Add `model_metadata` JSONB column to Result for PCA components, preprocessing params
- **Phase 2**: Create separate `spectral_points` table if JSONB performance degrades
- **Phase 3**: Add `role_permissions` table for granular RBAC
- **Phase 3**: Add `batch` table for grouping samples
- **Phase 4**: Add indexes for analytics queries

---

## Data Access Patterns

### Common Queries

**1. User Registration**:
```sql
INSERT INTO users (id, email, password_hash, role, created_at)
VALUES (uuid_generate_v4(), $1, $2, 'user', now())
RETURNING id;
```

**2. User Login (by email)**:
```sql
SELECT id, email, password_hash, role
FROM users
WHERE email = $1;
```

**3. Create Sample**:
```sql
INSERT INTO samples (id, user_id, filename, spectra_points, metadata, created_at)
VALUES (uuid_generate_v4(), $1, $2, $3, $4, now())
RETURNING id;
```

**4. Get User's Samples**:
```sql
SELECT id, filename, created_at
FROM samples
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

**5. Create Result**:
```sql
INSERT INTO results (id, sample_id, status, confidence, model_version, summary, created_at)
VALUES (uuid_generate_v4(), $1, $2, $3, $4, $5, now())
RETURNING id;
```

**6. Get Result by Sample ID** (with authorization):
```sql
SELECT r.id, r.status, r.confidence, r.model_version, r.summary, r.created_at,
       s.filename, s.user_id
FROM results r
JOIN samples s ON r.sample_id = s.id
WHERE s.id = $1 AND s.user_id = $2;
```

---

## Performance Considerations

### Indexing Strategy

- **Primary Keys**: UUID with B-tree index (default)
- **Foreign Keys**: Indexed for JOIN performance
- **Email Lookups**: Unique index on users.email
- **Chronological Queries**: Indexes on created_at columns
- **JSONB Queries**: GIN index on spectra_points (Phase 2 if needed)

### Expected Data Volume (Phase 1)

- **Users**: ~100 users (development/testing)
- **Samples**: ~1,000 samples
- **Results**: ~1,000 results (1:1 with samples)
- **Total DB Size**: ~500 MB (assuming 10KB per sample)

### Scalability Path (Future Phases)

- **Phase 2**: Partition samples table by created_at (monthly partitions)
- **Phase 3**: Read replicas for analytics queries
- **Phase 4**: Connection pooling (PgBouncer), query optimization

---

## Data Validation

### Application-Level Validation (Pydantic)

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Dict, Any
from datetime import datetime
import uuid

# User Registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    
# Sample Upload
class SpectralPoint(BaseModel):
    wavelength: float = Field(..., ge=200, le=2500)
    absorbance: float
    
class SampleCreate(BaseModel):
    filename: str = Field(..., max_length=255)
    spectra_points: List[SpectralPoint] = Field(..., max_items=10000)
    metadata: Dict[str, Any] = {}
    
    @validator('filename')
    def sanitize_filename(cls, v):
        # Remove path separators and parent directory references
        return v.replace('/', '_').replace('\\', '_').replace('..', '')
    
# Result Response
class ResultResponse(BaseModel):
    id: uuid.UUID
    status: str  # Enum: Authentic, Suspect, Verify
    confidence: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    summary: str
    created_at: datetime
```

---

## Security Considerations

### SQL Injection Prevention
- **SQLAlchemy ORM**: Parameterized queries by default
- **No Raw SQL**: Avoid raw SQL in Phase 1 unless necessary

### Data Ownership
- **Authorization**: Users can only access their own samples and results
- **Query Filters**: Always include `user_id` filter in WHERE clauses

### Sensitive Data
- **Password Hashing**: Bcrypt with 12 rounds
- **No PII Logging**: Never log password_hash or user email in plain text
- **JWT Secrets**: Stored in environment variables, never in database

---

**Phase 1 Data Model Complete** - Ready for API contract definition
