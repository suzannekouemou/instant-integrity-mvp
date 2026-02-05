# Implementation Tasks: Phase 2 - Chemometric Model Integration

**Feature Branch**: `002-phase2-chemometric-models`  
**Created**: 2025-11-24  
**Specification**: [spec.md](./spec.md)  
**Implementation Plan**: [plan.md](./plan.md)

## Overview

This document breaks down Phase 2 implementation into granular, executable tasks organized by user story. Each task is designed to be completable in 2-4 hours.

**Total Estimated Effort**: 18-24 days (3-4 weeks)  
**Total Tasks**: 72 tasks  
**Parallel Opportunities**: 35 parallelizable tasks marked with [P]

## Task Organization

Tasks are organized into phases:
1. **Setup** - ML dependencies and configuration
2. **Foundational** - Core ML components needed by all user stories
3. **User Story 1 (P1)** - Real Authenticity Analysis
4. **User Story 2 (P2)** - Model Training & Versioning
5. **User Story 3 (P3)** - Batch Processing
6. **User Story 4 (P3)** - Visualization & Explainability
7. **Polish** - Cross-cutting concerns and finalization

---

## Phase 1: Setup & ML Infrastructure (1-2 days)

**Goal**: Add ML dependencies, configuration files, and model storage structure

### Setup Tasks

- [ ] T001 Add ML dependencies to backend/requirements.txt (numpy, scipy, scikit-learn, matplotlib, joblib, PyYAML)
- [ ] T002 [P] Create backend/models/ directory for model artifacts with .gitkeep
- [ ] T003 [P] Create backend/config/ directory with .gitkeep
- [ ] T004 [P] Create backend/config/preprocessing.yaml with default parameters (baseline, noise reduction, normalization)
- [ ] T005 [P] Create backend/scripts/ directory for training scripts
- [ ] T006 [P] Create backend/app/ml/ module directory with __init__.py
- [ ] T007 [P] Create backend/models/README.md documenting model versioning and storage conventions
- [ ] T008 Create Alembic migration backend/alembic/versions/002_add_batch_table.py for Batch entity and Sample/Result updates
- [ ] T009 Run migration to create batches table and update samples/results tables
- [ ] T010 [P] Update backend/.env.example with ML-related environment variables (MODEL_PATH, CONFIG_PATH)

**Acceptance**: ML dependencies installed, config files created, database migrated

---

## Phase 2: Foundational ML Components (3-4 days)

**Goal**: Implement core preprocessing, PCA, and classifier modules used by all user stories

### Preprocessing Pipeline

- [ ] T011 [P] Create backend/app/ml/preprocess.py with baseline_als() function (Asymmetric Least Squares)
- [ ] T012 [P] Add baseline_polynomial() function to backend/app/ml/preprocess.py
- [ ] T013 [P] Add savgol_filter_wrapper() function to backend/app/ml/preprocess.py (Savitzky-Golay noise reduction)
- [ ] T014 [P] Add normalize_snv() function to backend/app/ml/preprocess.py (Standard Normal Variate)
- [ ] T015 [P] Add normalize_mean_center() function to backend/app/ml/preprocess.py
- [ ] T016 [P] Add preprocess_pipeline() orchestrator function to backend/app/ml/preprocess.py (loads config, applies steps)
- [ ] T017 [P] Create backend/tests/unit/test_preprocess.py with tests for each preprocessing function

### Feature Extraction (PCA)

- [ ] T018 [P] Create backend/app/ml/features.py with fit_pca() function (fits PCA model on training data)
- [ ] T019 [P] Add transform_pca() function to backend/app/ml/features.py (transforms new spectra)
- [ ] T020 [P] Add load_pca_model() function to backend/app/ml/features.py (loads from joblib file)
- [ ] T021 [P] Create backend/tests/unit/test_features.py with PCA fitting and transformation tests

### Classifier

- [ ] T022 [P] Create backend/app/ml/classifier.py with train_one_class_svm() function
- [ ] T023 [P] Add predict() function to backend/app/ml/classifier.py (returns status and confidence)
- [ ] T024 [P] Add calculate_confidence() function to backend/app/ml/classifier.py (converts decision function to 0-1 score)
- [ ] T025 [P] Add load_classifier() function to backend/app/ml/classifier.py
- [ ] T026 [P] Create backend/tests/unit/test_classifier.py with classifier training and prediction tests

### Model Storage & Versioning

- [ ] T027 [P] Create backend/app/ml/model_store.py with save_model() function (saves joblib + metadata JSON)
- [ ] T028 [P] Add load_latest_model() function to backend/app/ml/model_store.py (finds latest version by timestamp)
- [ ] T029 [P] Add list_model_versions() function to backend/app/ml/model_store.py
- [ ] T030 [P] Add generate_model_filename() function to backend/app/ml/model_store.py (semantic version + timestamp)
- [ ] T031 [P] Create backend/tests/unit/test_model_store.py with save/load/versioning tests

### Database Models

- [ ] T032 [P] Create backend/app/models/batch.py with Batch SQLAlchemy model
- [ ] T033 [P] Update backend/app/models/sample.py to add batch_id foreign key relationship
- [ ] T034 [P] Update backend/app/models/result.py to add preprocessing_params and pca_variance_explained columns
- [ ] T035 Update backend/app/models/__init__.py to import Batch model

**Acceptance**: All preprocessing, PCA, classifier, and model storage functions implemented and tested

---

## Phase 3: User Story 1 - Real Authenticity Analysis (4-5 days)

**User Story**: Real Authenticity Analysis with Chemometric Models (Priority P1)

**Goal**: Replace mock analysis with real chemometric pipeline (preprocessing → PCA → classifier)

**Independent Test**: Upload CSV → verify preprocessing applied → PCA transformed → real prediction returned with confidence

### Training Script & Initial Models

- [ ] T036 [US1] Create backend/scripts/train_model.py script with dataset loading from NIST/ChemSpider
- [ ] T037 [US1] Add preprocessing step to train_model.py (apply pipeline to training data)
- [ ] T038 [US1] Add PCA fitting step to train_model.py (fit on preprocessed data, save model)
- [ ] T039 [US1] Add classifier training step to train_model.py (train one-class SVM, save model)
- [ ] T040 [US1] Add cross-validation evaluation to train_model.py (5-fold CV, print metrics)
- [ ] T041 [US1] Add metadata generation to train_model.py (save version, date, metrics to JSON)
- [ ] T042 [US1] Run train_model.py to generate initial models (pca_v1.0.0_YYYYMMDD.joblib, classifier_v1.0.0_YYYYMMDD.joblib)

### Real Analysis Service

- [ ] T043 [US1] Update backend/app/services/analysis_service.py to replace mock with real pipeline
- [ ] T044 [US1] Add load_models() function to analysis_service.py (loads PCA + classifier on startup)
- [ ] T045 [US1] Add analyze_sample() function to analysis_service.py (preprocess → PCA → classify)
- [ ] T046 [US1] Update generate_result() to include preprocessing_params and pca_variance_explained
- [ ] T047 [P] [US1] Create backend/tests/unit/test_analysis_service.py with real pipeline tests

### API Integration

- [ ] T048 [US1] Update backend/app/routes/samples.py upload endpoint to use real analysis service
- [ ] T049 [US1] Add model version to upload response (from loaded model metadata)
- [ ] T050 [US1] Update backend/app/schemas/sample.py to include new result fields in response
- [ ] T051 [P] [US1] Create backend/tests/integration/test_real_analysis.py with end-to-end CSV upload test

### Regression Testing

- [ ] T052 [US1] Run all Phase 1 integration tests to verify no regression (authentication, single upload, results)
- [ ] T053 [US1] Add performance benchmark test (<10s for single sample analysis)

**US1 Acceptance Criteria**:
- ✓ Real preprocessing applied (baseline, noise reduction, normalization)
- ✓ PCA transformation with 95%+ variance explained
- ✓ One-class SVM prediction with confidence score
- ✓ Result includes model version and preprocessing params
- ✓ <10s analysis time for single sample
- ✓ Zero Phase 1 regression

---

## Phase 4: User Story 2 - Model Training & Versioning (2-3 days)

**User Story**: Model Training and Versioning (Priority P2)

**Goal**: Enable model retraining, versioning, and listing of available models

**Independent Test**: Run training script → verify new model version saved → verify model listing endpoint returns metadata

### Model Management API

- [ ] T054 [P] [US2] Create backend/app/routes/models.py with GET /api/v1/models endpoint
- [ ] T055 [P] [US2] Create backend/app/schemas/model.py with ModelVersion response schema
- [ ] T056 [US2] Implement list_models() in models.py route (calls model_store.list_model_versions())
- [ ] T057 [US2] Add model metadata parsing (read JSON files, return version info)
- [ ] T058 [US2] Register models router in backend/app/main.py under /api/v1/models

### Model Documentation

- [ ] T059 [P] [US2] Update backend/models/README.md with training instructions and hyperparameters
- [ ] T060 [P] [US2] Document model versioning rules (MAJOR.MINOR.PATCH) in README.md
- [ ] T061 [P] [US2] Add example metadata JSON to README.md

### Integration Tests

- [ ] T062 [US2] Create backend/tests/integration/test_model_management.py with model listing tests
- [ ] T063 [US2] Add test for model version comparison (latest vs older versions)
- [ ] T064 [US2] Add test for model metadata validation

**US2 Acceptance Criteria**:
- ✓ Training script generates versioned model artifacts
- ✓ Model metadata includes version, date, metrics
- ✓ Model listing endpoint returns all versions
- ✓ Latest model automatically loaded on startup

---

## Phase 5: User Story 3 - Batch Processing (3-4 days)

**User Story**: Batch Sample Processing (Priority P3)

**Goal**: Enable batch upload of multiple CSV files with async processing and progress tracking

**Independent Test**: Upload batch of 10 CSVs → verify batch_id returned → query status → verify all samples processed → retrieve batch summary

### Batch Processor

- [ ] T065 [P] [US3] Create backend/app/ml/batch_processor.py with BatchQueue class (asyncio.Queue wrapper)
- [ ] T066 [P] [US3] Add batch_worker() async function to batch_processor.py (processes samples from queue)
- [ ] T067 [P] [US3] Add update_batch_progress() function to batch_processor.py (updates database)
- [ ] T068 [P] [US3] Add start_batch_worker() startup function to batch_processor.py
- [ ] T069 [P] [US3] Create backend/tests/unit/test_batch_processor.py with queue and worker tests

### Batch API

- [ ] T070 [P] [US3] Create backend/app/routes/batch.py with POST /api/v1/analysis/batch endpoint
- [ ] T071 [P] [US3] Create backend/app/schemas/batch.py with BatchUpload request and BatchResponse schemas
- [ ] T072 [US3] Implement batch upload handler (validate files, create Batch record, queue samples)
- [ ] T073 [US3] Add GET /api/v1/analysis/batch/{batch_id} endpoint to batch.py
- [ ] T074 [US3] Implement batch status handler (return progress, summary, sample list)
- [ ] T075 [US3] Add batch summary calculation (authentic_count, suspect_count, avg_confidence)
- [ ] T076 [US3] Register batch router in backend/app/main.py under /api/v1/analysis
- [ ] T077 [US3] Initialize batch worker on app startup in backend/app/main.py

### Integration Tests

- [ ] T078 [US3] Create backend/tests/integration/test_batch_upload.py with batch upload tests
- [ ] T079 [US3] Add test for batch status endpoint (pending → processing → complete)
- [ ] T080 [US3] Add test for batch summary calculation
- [ ] T081 [US3] Add test for mixed valid/invalid files in batch
- [ ] T082 [US3] Add performance test (<2min for 50 samples)

**US3 Acceptance Criteria**:
- ✓ Batch upload accepts multiple CSV files
- ✓ Batch processing is asynchronous (non-blocking API)
- ✓ Batch status endpoint returns progress
- ✓ Batch summary includes aggregate statistics
- ✓ <2min processing time for 50 samples

---

## Phase 6: User Story 4 - Visualization & Explainability (2-3 days)

**User Story**: Visualization and Explainability (Priority P3)

**Goal**: Provide endpoints returning JSON plot data for spectra and PCA projections

**Independent Test**: Analyze sample → request spectra plot → verify raw/preprocessed data returned → request PCA plot → verify projection and cluster data returned

### Visualization Service

- [ ] T083 [P] [US4] Create backend/app/services/visualization_service.py with generate_spectra_plot() function
- [ ] T084 [P] [US4] Add generate_pca_plot() function to visualization_service.py (2D scatter: PC1 vs PC2)
- [ ] T085 [P] [US4] Add get_authentic_cluster() function to visualization_service.py (reference points from training)
- [ ] T086 [P] [US4] Add calculate_distance_to_manifold() function to visualization_service.py
- [ ] T087 [P] [US4] Add identify_key_wavelengths() function to visualization_service.py (top 5 contributors)

### Visualization API

- [ ] T088 [P] [US4] Create backend/app/routes/visualization.py with GET /api/v1/visualization/spectra/{sample_id} endpoint
- [ ] T089 [P] [US4] Create backend/app/schemas/visualization.py with SpectraPlot and PCAPlot response schemas
- [ ] T090 [US4] Implement spectra plot handler (return raw + preprocessed spectra JSON)
- [ ] T091 [US4] Add GET /api/v1/visualization/pca/{sample_id} endpoint to visualization.py
- [ ] T092 [US4] Implement PCA plot handler (return sample projection + authentic cluster)
- [ ] T093 [US4] Register visualization router in backend/app/main.py under /api/v1/visualization

### Integration Tests

- [ ] T094 [US4] Create backend/tests/integration/test_visualization.py with spectra plot tests
- [ ] T095 [US4] Add PCA plot endpoint tests
- [ ] T096 [US4] Add test for plot data format (compatible with Plotly/Chart.js)
- [ ] T097 [US4] Add performance test (<3s for visualization endpoints)

**US4 Acceptance Criteria**:
- ✓ Spectra plot endpoint returns raw + preprocessed data
- ✓ PCA plot endpoint returns sample projection + cluster
- ✓ Distance to manifold calculated and returned
- ✓ Key wavelengths identified
- ✓ <3s response time for visualization endpoints

---

## Phase 7: Polish & Cross-Cutting Concerns (1-2 days)

**Goal**: Finalize documentation, run full test suite, verify performance

### Documentation & Testing

- [ ] T098 Update backend/README.md with Phase 2 features and ML model information
- [ ] T099 Update backend/QUICKSTART.md with model training instructions
- [ ] T100 Create backend/models/README.md section on model evaluation metrics
- [ ] T101 Run full test suite (unit + integration) and verify 80%+ coverage
- [ ] T102 Run performance benchmarks (single sample, batch, visualization)
- [ ] T103 Verify all Phase 1 tests still pass (regression check)

### Configuration & Deployment

- [ ] T104 Verify config/preprocessing.yaml has sensible defaults for all sample types
- [ ] T105 Update docker-compose.yml if needed (no changes expected)
- [ ] T106 Update .env.example with all Phase 2 environment variables
- [ ] T107 Test Docker build with new ML dependencies

### API Documentation

- [ ] T108 Review FastAPI /docs endpoint for all new endpoints (batch, visualization, models)
- [ ] T109 Add API examples to README.md for new endpoints
- [ ] T110 Verify OpenAPI schema includes all new request/response models

**Final Acceptance**: All 43 requirements implemented, tests passing, documentation complete, performance targets met

---

## Task Dependencies & Parallel Execution

### Critical Path (Sequential)
1. Setup (Phase 1) → Must complete first
2. Foundational (Phase 2) → Blocks all user stories
3. US1 (Real Analysis) → Blocks US2, US3, US4 (needs working models)
4. US2 (Model Management) → Independent of US3, US4
5. US3 (Batch Processing) → Independent of US2, US4
6. US4 (Visualization) → Independent of US2, US3
7. Polish (Phase 7) → Final phase

### Parallel Opportunities

**Within Foundational Phase (Phase 2)**:
- All preprocessing functions can be developed in parallel (T011-T015)
- PCA and classifier modules can be developed in parallel (T018-T026)
- Model storage can be developed in parallel with preprocessing/PCA (T027-T031)
- Database models can be developed in parallel (T032-T034)

**Within User Story Phases**:
- Schemas, services, and unit tests within a story can be developed in parallel
- Integration tests written after endpoint implementation

**Example Parallel Workflow for US1**:
```
Developer A: Training script (T036-T042)
Developer B: Analysis service update (T043-T046)
Developer C: API integration (T048-T050)
→ Merge all
→ Together: Integration tests (T051-T053)
```

**Example Parallel Workflow for US3 + US4**:
```
Developer A: Batch processing (T065-T082)
Developer B: Visualization (T083-T097)
→ Both can proceed independently after US1 complete
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
**Recommended**: Complete through US1 (Real Analysis) for MVP demo
- Demonstrates: Real chemometric analysis with PCA + classifier
- Value: Actual authenticity detection replacing mock results
- Effort: ~10-12 days

### Incremental Delivery
1. **Week 1**: Setup + Foundational + US1 start (training script)
2. **Week 2**: US1 complete (real analysis) + US2 (model management)
3. **Week 3**: US3 (batch processing) + US4 start (visualization)
4. **Week 4**: US4 complete + Polish

### Testing Approach
- **Unit tests**: Written alongside or before implementation
- **Integration tests**: Written after endpoint implementation
- **Performance tests**: Run at end of each user story phase
- **Regression tests**: Run after each user story to verify Phase 1 still works

---

## Task Status Tracking

Update task status by checking boxes:
- `- [ ]` = Not started
- `- [x]` = Complete
- Add notes inline for blocked tasks

**Example**:
```
- [x] T001 Add ML dependencies to requirements.txt ✓ Completed 2025-11-24
- [ ] T002 [P] Create models/ directory (Blocked: awaiting disk space)
```

---

**Total Tasks**: 110  
**Estimated Completion**: 18-24 days (3-4 weeks)  
**Next Step**: Begin with T001 and work sequentially through Setup phase

**Ready for**: `/speckit.implement` to start implementation
