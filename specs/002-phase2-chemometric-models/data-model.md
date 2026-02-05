# Data Model: Phase 2 - Chemometric Model Integration

**Feature**: Phase 2 - Chemometric Model Integration  
**Date**: 2025-11-24

## Overview

Phase 2 extends the Phase 1 data model with batch processing support and enhanced result metadata. No changes to existing User, EmailVerificationToken, or Sample entities (except adding optional batch_id to Sample).

---

## New Entity: Batch

Represents a batch upload of multiple samples for processing.

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique batch identifier |
| user_id | UUID | NOT NULL, FK(users.id) | Owner of the batch |
| total_samples | INTEGER | NOT NULL | Total number of samples in batch |
| processed_count | INTEGER | DEFAULT 0 | Number of samples processed so far |
| status | VARCHAR(20) | NOT NULL, CHECK | Batch processing status |
| created_at | TIMESTAMP | DEFAULT NOW() | Batch creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

### Status Values
- `pending`: Batch created, not yet processing
- `processing`: Worker is processing samples
- `complete`: All samples processed successfully
- `failed`: Batch processing failed (partial results may exist)

### Relationships
- **One-to-Many** with Sample: A batch contains multiple samples
- **Many-to-One** with User: A user can create multiple batches

### Indexes
```sql
CREATE INDEX idx_batches_user_id ON batches(user_id);
CREATE INDEX idx_batches_status ON batches(status);
CREATE INDEX idx_batches_created_at ON batches(created_at DESC);
```

### SQLAlchemy Model
```python
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models import Base
import uuid

class Batch(Base):
    __tablename__ = "batches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_samples = Column(Integer, nullable=False)
    processed_count = Column(Integer, default=0)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="batches")
    samples = relationship("Sample", back_populates="batch")
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'processing', 'complete', 'failed')", name="ck_batch_status"),
    )
```

---

## Updated Entity: Sample

Adds optional batch_id to link samples to batches.

### New Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| batch_id | UUID | NULLABLE, FK(batches.id) | Optional batch association |

### Migration
```sql
ALTER TABLE samples ADD COLUMN batch_id UUID REFERENCES batches(id) ON DELETE SET NULL;
CREATE INDEX idx_samples_batch_id ON samples(batch_id);
```

### Updated SQLAlchemy Model
```python
class Sample(Base):
    __tablename__ = "samples"
    
    # ... existing fields ...
    batch_id = Column(UUID(as_uuid=True), ForeignKey("batches.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    batch = relationship("Batch", back_populates="samples")
```

---

## Updated Entity: Result

Adds preprocessing parameters and PCA variance explained to results.

### New Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| preprocessing_params | JSONB | NULLABLE | Preprocessing configuration used |
| pca_variance_explained | FLOAT | NULLABLE | Total variance explained by PCA |

### Migration
```sql
ALTER TABLE results ADD COLUMN preprocessing_params JSONB;
ALTER TABLE results ADD COLUMN pca_variance_explained FLOAT;
```

### Updated SQLAlchemy Model
```python
from sqlalchemy.dialects.postgresql import JSONB

class Result(Base):
    __tablename__ = "results"
    
    # ... existing fields ...
    preprocessing_params = Column(JSONB, nullable=True)
    pca_variance_explained = Column(Float, nullable=True)
```

### Example preprocessing_params JSON
```json
{
  "baseline_method": "als",
  "als_lambda": 100000,
  "als_p": 0.01,
  "filter_window": 11,
  "filter_order": 3,
  "normalization": "snv"
}
```

---

## File-Based Entities (Not in Database)

### PCAModel (Joblib Artifact)

Stored in `/models/pca_v{version}_{date}.joblib`

**Attributes** (scikit-learn PCA object):
- `n_components_`: Number of components retained
- `explained_variance_ratio_`: Variance explained by each component
- `components_`: Principal component loadings
- `mean_`: Mean of training data

### Classifier (Joblib Artifact)

Stored in `/models/classifier_v{version}_{date}.joblib`

**Attributes** (scikit-learn OneClassSVM object):
- `kernel`: Kernel type (rbf)
- `gamma`: Kernel coefficient
- `nu`: Upper bound on fraction of outliers
- `support_vectors_`: Support vectors from training

### ModelMetadata (JSON File)

Stored in `/models/metadata_v{version}_{date}.json`

**Schema**:
```json
{
  "version": "1.0.0",
  "training_date": "2025-11-24",
  "pca_model": "pca_v1.0.0_20251124.joblib",
  "classifier_model": "classifier_v1.0.0_20251124.joblib",
  "dataset_summary": {
    "source": "NIST Chemistry WebBook",
    "num_samples": 150,
    "sample_types": ["flour", "spice", "herb"],
    "wavelength_range": [400, 2500]
  },
  "pca_metrics": {
    "n_components": 7,
    "variance_explained": 0.96,
    "explained_variance_ratio": [0.45, 0.25, 0.12, 0.08, 0.04, 0.01, 0.01]
  },
  "classifier_metrics": {
    "cv_accuracy": 0.91,
    "cv_std": 0.03,
    "kernel": "rbf",
    "gamma": "scale",
    "nu": 0.1
  },
  "preprocessing_config": {
    "baseline_method": "als",
    "filter_window": 11,
    "normalization": "snv"
  }
}
```

---

## Entity Relationships Diagram

```
User (Phase 1)
  ├── 1:N → Sample (Phase 1, updated)
  ├── 1:N → Result (Phase 1, updated)
  └── 1:N → Batch (Phase 2, new)

Batch (Phase 2, new)
  ├── N:1 → User
  └── 1:N → Sample

Sample (Phase 1, updated)
  ├── N:1 → User
  ├── N:1 → Batch (optional)
  └── 1:1 → Result

Result (Phase 1, updated)
  └── 1:1 → Sample

[File System]
  ├── PCAModel (joblib)
  ├── Classifier (joblib)
  └── ModelMetadata (JSON)
```

---

## Database Migration Script

**File**: `backend/alembic/versions/002_add_batch_table.py`

```python
"""Add batch table and update sample/result

Revision ID: 002
Revises: 001
Create Date: 2025-11-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Create batches table
    op.create_table(
        'batches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_samples', sa.Integer(), nullable=False),
        sa.Column('processed_count', sa.Integer(), server_default='0'),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()')),
        sa.CheckConstraint("status IN ('pending', 'processing', 'complete', 'failed')", name='ck_batch_status')
    )
    
    # Create indexes
    op.create_index('idx_batches_user_id', 'batches', ['user_id'])
    op.create_index('idx_batches_status', 'batches', ['status'])
    op.create_index('idx_batches_created_at', 'batches', ['created_at'], postgresql_ops={'created_at': 'DESC'})
    
    # Add batch_id to samples
    op.add_column('samples', sa.Column('batch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('batches.id', ondelete='SET NULL'), nullable=True))
    op.create_index('idx_samples_batch_id', 'samples', ['batch_id'])
    
    # Add new columns to results
    op.add_column('results', sa.Column('preprocessing_params', postgresql.JSONB(), nullable=True))
    op.add_column('results', sa.Column('pca_variance_explained', sa.Float(), nullable=True))

def downgrade():
    # Remove columns from results
    op.drop_column('results', 'pca_variance_explained')
    op.drop_column('results', 'preprocessing_params')
    
    # Remove batch_id from samples
    op.drop_index('idx_samples_batch_id', 'samples')
    op.drop_column('samples', 'batch_id')
    
    # Drop batches table
    op.drop_index('idx_batches_created_at', 'batches')
    op.drop_index('idx_batches_status', 'batches')
    op.drop_index('idx_batches_user_id', 'batches')
    op.drop_table('batches')
```

---

## Data Validation Rules

### Batch
- `total_samples` must be > 0
- `processed_count` must be >= 0 and <= `total_samples`
- `status` transitions: pending → processing → complete/failed

### Sample (updated)
- `batch_id` is optional (NULL for single uploads)
- If `batch_id` is set, sample must belong to authenticated user's batch

### Result (updated)
- `preprocessing_params` must be valid JSON if present
- `pca_variance_explained` must be between 0 and 1 if present

---

## Query Patterns

### Get batch with samples
```python
batch = db.query(Batch).filter(Batch.id == batch_id).first()
samples = db.query(Sample).filter(Sample.batch_id == batch_id).all()
```

### Get batch summary
```python
from sqlalchemy import func

summary = db.query(
    func.count(Sample.id).label('total'),
    func.sum(case((Result.status == 'Authentic', 1), else_=0)).label('authentic_count'),
    func.avg(Result.confidence).label('avg_confidence')
).join(Result).filter(Sample.batch_id == batch_id).first()
```

### List user's batches
```python
batches = db.query(Batch).filter(
    Batch.user_id == user_id
).order_by(Batch.created_at.desc()).all()
```

---

## Storage Estimates

### Database Growth
- **Batch**: ~200 bytes per record
- **Sample**: +16 bytes (batch_id UUID)
- **Result**: +500 bytes (preprocessing_params JSONB)

**Example**: 1000 batches × 50 samples = 50,000 samples
- Batches: 200 KB
- Samples: 800 KB (batch_id only)
- Results: 25 MB (preprocessing_params)

### File System Growth
- **PCA model**: ~5 MB per version
- **Classifier model**: ~10 MB per version
- **Metadata**: ~5 KB per version

**Example**: 10 model versions = 150 MB total

---

**Status**: Data model complete, ready for API contract generation
