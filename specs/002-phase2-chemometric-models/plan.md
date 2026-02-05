# Implementation Plan: Phase 2 - Chemometric Model Integration

**Branch**: `002-phase2-chemometric-models` | **Date**: 2025-11-24 | **Spec**: [spec.md](./spec.md)

## Summary

Phase 2 replaces mock authenticity results with real chemometric analysis using PCA and one-class SVM classifier. Adds preprocessing pipeline (baseline correction, noise reduction, normalization), model training/versioning system, batch processing with async queue, and visualization endpoints returning JSON plot data. Uses open-source spectral datasets for training, configuration files for preprocessing parameters, and semantic versioning for model artifacts.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI 0.104+, numpy 1.24+, scipy 1.11+, scikit-learn 1.3+, matplotlib 3.7+, joblib 1.3+, PyYAML 6.0+  
**Storage**: PostgreSQL 15+ (existing), filesystem for model artifacts (`/models` directory)  
**Testing**: pytest 7.4+, pytest-asyncio 0.23+, pytest-cov 4.1+  
**Target Platform**: Linux server (Docker containers)  
**Project Type**: Web API (backend extension)  
**Performance Goals**: <10s single sample analysis, <2min batch of 50 samples, <3s visualization endpoints  
**Constraints**: 95% preprocessing success rate, 90% classifier accuracy (cross-validation), zero Phase 1 regression  
**Scale/Scope**: 4 new user stories, 43 new functional requirements, ~2000-3000 lines Python, 3-4 weeks

## Constitution Check ✅ PASSED

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All principles satisfied:

- ✅ **Security-First**: Maintains Phase 1 authentication/authorization; no new security risks
- ✅ **Zero-Cost**: All dependencies open-source; no cloud ML services
- ✅ **TDD**: Unit tests for preprocessing/PCA/classifier, integration tests for new endpoints
- ✅ **Phased Delivery**: Clear Phase 2 scope; no Phase 3 features (frontend UI)
- ✅ **Data Integrity**: Model versioning, preprocessing logging, cross-validation
- ✅ **API-First**: REST endpoints for batch, visualization, model listing
- ✅ **Observability**: Logging for model loading, preprocessing failures, batch progress

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-chemometric-models/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (API contracts)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── ml/                      # NEW: Machine learning module
│   │   ├── __init__.py
│   │   ├── preprocess.py        # Baseline correction, noise reduction, normalization
│   │   ├── features.py          # PCA transformation
│   │   ├── classifier.py        # One-class SVM classifier
│   │   ├── model_store.py       # Model loading/versioning
│   │   └── batch_processor.py   # Async batch queue
│   ├── services/
│   │   ├── analysis_service.py  # UPDATED: Replace mock with real pipeline
│   │   └── visualization_service.py  # NEW: Plot data generation
│   ├── routes/
│   │   ├── samples.py           # UPDATED: Maintain compatibility
│   │   ├── batch.py             # NEW: Batch upload/status endpoints
│   │   ├── visualization.py     # NEW: Spectra/PCA plot endpoints
│   │   └── models.py            # NEW: Model listing endpoint
│   ├── schemas/
│   │   ├── batch.py             # NEW: Batch request/response schemas
│   │   └── visualization.py     # NEW: Plot data schemas
│   └── models/
│       └── batch.py             # NEW: Batch database model
├── tests/
│   ├── unit/
│   │   ├── test_preprocess.py   # NEW: Preprocessing tests
│   │   ├── test_features.py     # NEW: PCA tests
│   │   ├── test_classifier.py   # NEW: Classifier tests
│   │   └── test_batch_processor.py  # NEW: Batch queue tests
│   └── integration/
│       ├── test_real_analysis.py    # NEW: End-to-end pipeline test
│       ├── test_batch_upload.py     # NEW: Batch API tests
│       └── test_visualization.py    # NEW: Visualization endpoint tests
├── models/                      # NEW: Model artifacts directory
│   ├── README.md                # Model documentation
│   ├── pca_v1.0.0_20251124.joblib
│   ├── classifier_v1.0.0_20251124.joblib
│   └── metadata_v1.0.0_20251124.json
├── config/                      # NEW: Configuration directory
│   └── preprocessing.yaml       # Preprocessing parameters
├── scripts/                     # NEW: Training scripts
│   └── train_model.py           # Model training script
└── alembic/versions/
    └── 002_add_batch_table.py   # NEW: Batch table migration
```

**Structure Decision**: Extends existing backend structure with new `/ml` module for chemometric logic, `/models` directory for artifacts, `/config` for parameters, and `/scripts` for training. Maintains Phase 1 architecture patterns (routes → services → models).

## Complexity Tracking

> No constitution violations - all complexity justified by core scientific requirements

---

## Phase 0: Research & Technology Decisions

### Research Tasks

1. **Open-source spectral datasets**
   - Decision: Use NIST Chemistry WebBook + ChemSpider for NIR/FTIR spectra
   - Rationale: Free, well-documented, covers flour/spice/herb categories
   - Alternatives: Synthetic data (less realistic), partner data (requires agreements)

2. **Baseline correction methods**
   - Decision: Asymmetric Least Squares (ALS) as default, polynomial fitting as fallback
   - Rationale: ALS handles fluorescence better, polynomial simpler for clean spectra
   - Alternatives: Wavelet transform (too complex for Phase 2)

3. **Savitzky-Golay filter parameters**
   - Decision: Window size 11, polynomial order 3 (configurable via YAML)
   - Rationale: Standard for spectral smoothing, balances noise reduction vs signal preservation
   - Alternatives: Moving average (loses peak shape), Gaussian filter (requires sigma tuning)

4. **PCA variance threshold**
   - Decision: Retain components explaining 95% variance
   - Rationale: Industry standard, typically 5-10 components for spectral data
   - Alternatives: Fixed number of components (less adaptive), 99% variance (overfitting risk)

5. **One-class SVM kernel**
   - Decision: RBF kernel with gamma='scale'
   - Rationale: Handles non-linear boundaries, auto-scales with features
   - Alternatives: Linear kernel (underfits spectral data), polynomial (slower)

6. **Batch processing architecture**
   - Decision: asyncio.Queue with single background worker
   - Rationale: Simple, sufficient for 50 samples, no external dependencies
   - Alternatives: Celery+Redis (overkill for Phase 2), synchronous (blocks API)

7. **Model versioning strategy**
   - Decision: Semantic versioning + timestamp (e.g., `pca_v1.0.0_20251124.joblib`)
   - Rationale: Clear version progression, easy rollback, timestamp for uniqueness
   - Alternatives: Git hash (not human-readable), incremental numbers (no semantic meaning)

8. **Cross-validation approach**
   - Decision: 5-fold stratified CV for one-class SVM
   - Rationale: Balances bias-variance, standard for small datasets
   - Alternatives: 10-fold (slower, minimal accuracy gain), leave-one-out (too slow)

---

## Phase 1: Data Model & API Contracts

### Database Schema Changes

**New Entity: Batch**

```sql
CREATE TABLE batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_samples INTEGER NOT NULL,
    processed_count INTEGER DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'processing', 'complete', 'failed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_batches_user_id ON batches(user_id);
CREATE INDEX idx_batches_status ON batches(status);
```

**Updated Entity: Sample**

```sql
-- Add batch_id column (nullable for backward compatibility)
ALTER TABLE samples ADD COLUMN batch_id UUID REFERENCES batches(id) ON DELETE SET NULL;
CREATE INDEX idx_samples_batch_id ON samples(batch_id);
```

**Updated Entity: Result**

```sql
-- Add preprocessing_params column
ALTER TABLE results ADD COLUMN preprocessing_params JSONB;
-- Add pca_variance_explained column
ALTER TABLE results ADD COLUMN pca_variance_explained FLOAT;
```

### API Contracts

#### POST /api/v1/analysis/batch

**Request** (multipart/form-data):
```json
{
  "files": ["file1.csv", "file2.csv", ...],
  "sample_type": "flour"  // enum: flour, spice, herb, other
}
```

**Response** (201 Created):
```json
{
  "batch_id": "uuid",
  "total_samples": 10,
  "status": "pending",
  "created_at": "2025-11-24T14:00:00Z"
}
```

#### GET /api/v1/analysis/batch/{batch_id}

**Response** (200 OK):
```json
{
  "batch_id": "uuid",
  "total_samples": 10,
  "processed_count": 7,
  "status": "processing",
  "summary": {
    "authentic_count": 5,
    "suspect_count": 2,
    "avg_confidence": 0.87
  },
  "samples": [
    {
      "sample_id": "uuid",
      "filename": "sample1.csv",
      "status": "Authentic",
      "confidence": 0.92
    }
  ]
}
```

#### GET /api/v1/visualization/spectra/{sample_id}

**Response** (200 OK):
```json
{
  "sample_id": "uuid",
  "raw_spectra": {
    "wavelengths": [400, 401, ...],
    "absorbance": [0.1, 0.12, ...]
  },
  "preprocessed_spectra": {
    "wavelengths": [400, 401, ...],
    "absorbance": [0.09, 0.11, ...]
  },
  "preprocessing_params": {
    "baseline_method": "als",
    "filter_window": 11,
    "normalization": "snv"
  }
}
```

#### GET /api/v1/visualization/pca/{sample_id}

**Response** (200 OK):
```json
{
  "sample_id": "uuid",
  "sample_projection": {"pc1": 2.3, "pc2": -1.1},
  "authentic_cluster": [
    {"pc1": 2.1, "pc2": -0.9},
    {"pc1": 2.5, "pc2": -1.3}
  ],
  "variance_explained": [0.45, 0.25],
  "distance_to_manifold": 0.15
}
```

#### GET /api/v1/models

**Response** (200 OK):
```json
{
  "models": [
    {
      "version": "v1.0.0",
      "training_date": "2025-11-24",
      "pca_components": 7,
      "variance_explained": 0.96,
      "cv_score": 0.91,
      "is_active": true
    }
  ]
}
```

### Configuration Files

**config/preprocessing.yaml**:
```yaml
baseline:
  method: als  # Options: als, polynomial
  polynomial_degree: 3  # Used if method=polynomial
  als_lambda: 1e5
  als_p: 0.01

noise_reduction:
  method: savgol  # Options: savgol, none
  window_size: 11
  polynomial_order: 3

normalization:
  method: snv  # Options: snv, mean_center, none

wavelength:
  min: 400  # nm
  max: 2500  # nm
  tolerance: 5  # nm for range matching
```

---

## Phase 2: Implementation Phases

### Phase 2.1: Preprocessing Pipeline (Week 1)

**Goal**: Implement baseline correction, noise reduction, normalization

**Deliverables**:
- `app/ml/preprocess.py` with functions: `baseline_als()`, `baseline_polynomial()`, `savgol_filter()`, `normalize_snv()`, `normalize_mean_center()`
- `config/preprocessing.yaml` with default parameters
- Unit tests for each preprocessing function
- Integration test for full preprocessing pipeline

**Acceptance**: Preprocessing handles 95% of test spectra without errors

### Phase 2.2: PCA & Feature Extraction (Week 1-2)

**Goal**: Implement PCA transformation and model storage

**Deliverables**:
- `app/ml/features.py` with `fit_pca()`, `transform_pca()`, `load_pca_model()`
- `app/ml/model_store.py` with `save_model()`, `load_model()`, `list_models()`
- Model metadata JSON schema
- Unit tests for PCA fitting/transformation
- Model versioning tests

**Acceptance**: PCA explains 95%+ variance, models load correctly with version tracking

### Phase 2.3: Classifier Training & Inference (Week 2)

**Goal**: Train one-class SVM and integrate into analysis pipeline

**Deliverables**:
- `app/ml/classifier.py` with `train_one_class_svm()`, `predict()`, `calculate_confidence()`
- `scripts/train_model.py` training script with cross-validation
- Training dataset acquisition (NIST/ChemSpider)
- Unit tests for classifier
- Model evaluation metrics

**Acceptance**: Classifier achieves 90%+ accuracy on cross-validation

### Phase 2.4: Real Analysis Integration (Week 2-3)

**Goal**: Replace mock analysis with real chemometric pipeline

**Deliverables**:
- Update `app/services/analysis_service.py` to use real pipeline
- Update `app/routes/samples.py` to maintain backward compatibility
- Integration tests for end-to-end analysis
- Performance testing (<10s per sample)

**Acceptance**: Single-sample upload returns real predictions, Phase 1 tests still pass

### Phase 2.5: Batch Processing (Week 3)

**Goal**: Implement async batch upload and processing

**Deliverables**:
- `app/ml/batch_processor.py` with asyncio.Queue worker
- `app/routes/batch.py` with batch endpoints
- `app/schemas/batch.py` with request/response schemas
- Database migration for `batches` table
- Integration tests for batch API

**Acceptance**: Batch of 50 samples processes in <2 minutes

### Phase 2.6: Visualization Endpoints (Week 3-4)

**Goal**: Add endpoints returning JSON plot data

**Deliverables**:
- `app/services/visualization_service.py` with plot data generation
- `app/routes/visualization.py` with spectra/PCA endpoints
- `app/schemas/visualization.py` with plot data schemas
- Integration tests for visualization endpoints

**Acceptance**: Visualization endpoints return data in <3s, compatible with Plotly/Chart.js

### Phase 2.7: Model Management (Week 4)

**Goal**: Add model listing endpoint and documentation

**Deliverables**:
- `app/routes/models.py` with model listing endpoint
- `models/README.md` with model documentation
- Model metadata tracking
- Integration tests for model endpoint

**Acceptance**: Model endpoint lists all versions with metadata

---

## Testing Strategy

### Unit Tests (New)
- `test_preprocess.py`: Each preprocessing function with edge cases
- `test_features.py`: PCA fitting, transformation, variance calculation
- `test_classifier.py`: Training, prediction, confidence scoring
- `test_model_store.py`: Save/load/version operations
- `test_batch_processor.py`: Queue operations, worker logic

### Integration Tests (New)
- `test_real_analysis.py`: Full pipeline from CSV to prediction
- `test_batch_upload.py`: Batch API endpoints
- `test_visualization.py`: Visualization endpoints
- `test_model_management.py`: Model listing endpoint

### Regression Tests
- All Phase 1 tests must pass (authentication, single upload, results)
- Performance benchmarks: <10s single sample, <2min batch of 50

---

## Dependencies

### New Python Packages
```txt
numpy>=1.24.0
scipy>=1.11.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
joblib>=1.3.0
PyYAML>=6.0
```

### External Data
- NIST Chemistry WebBook spectral data (free download)
- ChemSpider API (free tier, 1000 requests/day)

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Training data quality | High | Validate spectra before training, use multiple sources |
| Model overfitting | Medium | Cross-validation, variance threshold tuning |
| Batch processing memory | Medium | Process samples sequentially, limit queue size |
| Preprocessing failures | High | Robust error handling, fallback to simpler methods |
| Performance regression | High | Benchmark tests, profile slow operations |

---

## Success Metrics

- ✅ All 43 functional requirements implemented
- ✅ 90%+ classifier accuracy (cross-validation)
- ✅ <10s single sample analysis
- ✅ <2min batch of 50 samples
- ✅ Zero Phase 1 regression
- ✅ 80%+ code coverage
- ✅ All integration tests passing

---

**Plan Status**: Ready for task breakdown (`/speckit.tasks`)
