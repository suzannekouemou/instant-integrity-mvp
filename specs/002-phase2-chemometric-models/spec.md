# Feature Specification: Phase 2 - Chemometric Model Integration

**Feature Branch**: `002-phase2-chemometric-models`  
**Created**: 2025-11-24  
**Status**: Draft  
**Input**: User description: "Phase 2: Chemometric Model Integration - Add real preprocessing (baseline correction, noise reduction, PCA), train simple classifier (authentic vs suspect), replace mock results with real predictions, add batch processing endpoints"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Real Authenticity Analysis with Chemometric Models (Priority: P1)

An authenticated user uploads spectral data and receives a real authenticity prediction based on trained chemometric models (PCA + classifier) instead of mock results.

**Why this priority**: This is the core scientific value proposition. Without real models, the platform is just a data storage system. This delivers the actual authenticity detection capability.

**Independent Test**: Can be fully tested by uploading a CSV file, verifying preprocessing is applied, PCA transformation occurs, classifier predicts, and real confidence score is returned. Delivers immediate scientific value.

**Acceptance Scenarios**:

1. **Given** authenticated user with valid CSV spectral data, **When** user uploads sample, **Then** system applies baseline correction and noise reduction to raw spectra
2. **Given** preprocessed spectral data, **When** system performs analysis, **Then** PCA transformation is applied and principal components are extracted
3. **Given** PCA-transformed data, **When** classifier runs, **Then** real authenticity prediction (Authentic/Suspect) is returned with confidence score
4. **Given** completed analysis, **When** result is generated, **Then** result includes model version, preprocessing parameters, and PCA variance explained
5. **Given** suspect sample detected, **When** confidence is below threshold, **Then** system recommends "Verify" status for lab confirmation

---

### User Story 2 - Model Training and Versioning (Priority: P2)

A data scientist or admin can train new chemometric models using curated datasets, version them, and deploy them to replace existing models.

**Why this priority**: Essential for model improvement and adaptation to new sample types. Without this, models remain static and cannot improve over time.

**Independent Test**: Can be fully tested by running training script with dataset, verifying model artifacts are saved, metadata is recorded, and new model version is available for inference.

**Acceptance Scenarios**:

1. **Given** curated training dataset (authentic samples), **When** training script runs, **Then** PCA model is fitted and saved with variance explained metrics
2. **Given** fitted PCA model, **When** classifier training runs, **Then** one-class SVM or classifier is trained and saved with evaluation metrics
3. **Given** trained models, **When** artifacts are persisted, **Then** model version, training date, dataset summary, and performance metrics are recorded
4. **Given** new model version, **When** system loads models, **Then** inference uses latest version and result includes model_version identifier
5. **Given** multiple model versions, **When** admin queries, **Then** system can list all versions with metadata and performance comparison

---

### User Story 3 - Batch Sample Processing (Priority: P3)

An authenticated user uploads multiple CSV files in a batch and receives aggregated analysis results for the entire batch.

**Why this priority**: Improves efficiency for quality control workflows where multiple samples are tested together. Adds convenience but core single-sample analysis is more critical.

**Independent Test**: Can be fully tested by uploading multiple CSV files, verifying each is processed independently, and batch summary is generated with aggregate statistics.

**Acceptance Scenarios**:

1. **Given** authenticated user with multiple CSV files, **When** user uploads batch, **Then** system validates and queues all samples for processing
2. **Given** queued batch samples, **When** processing runs, **Then** each sample is analyzed independently with real models
3. **Given** completed batch analysis, **When** results are aggregated, **Then** batch summary includes total samples, authentic count, suspect count, average confidence
4. **Given** batch with mixed results, **When** user retrieves batch summary, **Then** system highlights suspect samples requiring attention
5. **Given** batch processing in progress, **When** user queries status, **Then** system returns progress percentage and estimated completion time

---

### User Story 4 - Visualization and Explainability (Priority: P3)

An authenticated user views spectral plots, PCA projections, and model explanations to understand why a sample was classified as authentic or suspect.

**Why this priority**: Enhances trust and scientific transparency. Users can validate results and understand model decisions. Less critical than core analysis functionality.

**Independent Test**: Can be fully tested by requesting visualization endpoints after analysis, verifying plots are generated, and PCA projections show sample position relative to authentic cluster.

**Acceptance Scenarios**:

1. **Given** analyzed sample, **When** user requests spectra plot, **Then** system returns raw vs preprocessed spectra visualization
2. **Given** PCA-transformed sample, **When** user requests PCA plot, **Then** system returns 2D/3D scatter plot showing sample position vs authentic cluster
3. **Given** classification result, **When** user requests explanation, **Then** system returns distance to authentic manifold and key wavelength contributions
4. **Given** batch analysis, **When** user requests batch visualization, **Then** system returns PCA plot with all batch samples color-coded by status
5. **Given** suspect sample, **When** user views explanation, **Then** system highlights spectral regions deviating from authentic profile

---

### Edge Cases

- What happens when uploaded spectra have different wavelength ranges than training data?
- How does system handle spectra with missing wavelength points or gaps?
- What happens when PCA variance explained is unusually low (poor data quality)?
- How does system respond when classifier confidence is exactly at threshold boundary?
- What happens when model files are corrupted or missing?
- How does system handle extremely noisy spectra that fail preprocessing?
- What happens when batch upload includes mix of valid and invalid CSV files?
- How does system manage memory when processing large batches (100+ samples)?

## Requirements *(mandatory)*

### Functional Requirements

#### Preprocessing Pipeline

- **FR-001**: System MUST apply baseline correction to raw spectral data using polynomial fitting or asymmetric least squares (ALS)
- **FR-002**: System MUST apply noise reduction using Savitzky-Golay filter with window size and polynomial order from configuration file (YAML/JSON)
- **FR-003**: System MUST apply scatter correction using Standard Normal Variate (SNV) or mean-centering normalization
- **FR-004**: System MUST validate spectral data wavelength range matches training data range (±5nm tolerance)
- **FR-005**: System MUST handle missing wavelength points by interpolation or rejection based on gap size
- **FR-006**: System MUST log preprocessing parameters (baseline method, filter window, normalization) with each result
- **FR-006a**: System MUST load preprocessing parameters from configuration file (e.g., `config/preprocessing.yaml`) with sensible defaults

#### Feature Extraction

- **FR-007**: System MUST perform PCA transformation on preprocessed spectra using fitted PCA model
- **FR-008**: System MUST retain principal components explaining at least 95% of variance
- **FR-009**: System MUST store PCA model with explained variance ratios and component loadings
- **FR-010**: System MUST validate input spectra dimensionality matches PCA model expectations
- **FR-011**: System MUST return principal component scores for each analyzed sample

#### Classification

- **FR-012**: System MUST classify samples using trained one-class SVM or binary classifier
- **FR-013**: System MUST return classification status: Authentic, Suspect, or Verify
- **FR-014**: System MUST calculate confidence score (0-1) based on decision function or probability
- **FR-015**: System MUST apply configurable thresholds: Authentic (>0.8), Suspect (<0.5), Verify (0.5-0.8)
- **FR-016**: System MUST include model version identifier in every result
- **FR-017**: System MUST handle edge cases where classifier returns NaN or infinite values

#### Model Training & Versioning

- **FR-018**: System MUST provide training script accepting CSV dataset of authentic samples
- **FR-019**: System MUST fit PCA model on training data and save as joblib artifact
- **FR-020**: System MUST train classifier (one-class SVM or logistic regression) and save as joblib artifact
- **FR-021**: System MUST generate model metadata: version, training_date, dataset_summary, performance_metrics (cross-validation scores using 5-fold or 10-fold CV)
- **FR-022**: System MUST store model artifacts in `/models` directory with semantic versioning and timestamp naming (e.g., `pca_v1.0.0_20251124.joblib`, `classifier_v1.0.0_20251124.joblib`)
- **FR-023**: System MUST validate model artifacts on load (check file integrity, compatibility)
- **FR-024**: System MUST support multiple model versions and load latest by default

#### Batch Processing

- **FR-025**: System MUST provide endpoint accepting multiple CSV files for batch upload
- **FR-026**: System MUST validate each file independently and reject invalid files without blocking batch
- **FR-027**: System MUST process batch samples asynchronously and return batch_id for status tracking
- **FR-028**: System MUST generate batch summary with aggregate statistics: total, authentic_count, suspect_count, avg_confidence
- **FR-029**: System MUST provide endpoint to query batch processing status and progress
- **FR-030**: System MUST link individual sample results to batch_id for retrieval

#### Visualization & Explainability

- **FR-031**: System MUST provide endpoint returning raw vs preprocessed spectra plot data (JSON format)
- **FR-032**: System MUST provide endpoint returning PCA projection plot data (2D scatter: PC1 vs PC2)
- **FR-033**: System MUST include authentic cluster reference points in PCA plot for comparison
- **FR-034**: System MUST calculate and return distance to authentic manifold for each sample
- **FR-035**: System MUST identify top 5 wavelength regions contributing most to classification decision
- **FR-036**: System MUST return plot data in JSON format compatible with frontend charting libraries (Plotly, Chart.js)

#### API Enhancements

- **FR-037**: System MUST replace mock analysis service with real chemometric pipeline
- **FR-038**: System MUST add POST `/api/v1/analysis/batch` endpoint for batch uploads
- **FR-039**: System MUST add GET `/api/v1/analysis/batch/{batch_id}` endpoint for batch status
- **FR-040**: System MUST add GET `/api/v1/visualization/spectra/{sample_id}` endpoint for spectra plots
- **FR-041**: System MUST add GET `/api/v1/visualization/pca/{sample_id}` endpoint for PCA plots
- **FR-042**: System MUST add GET `/api/v1/models` endpoint listing available model versions
- **FR-043**: System MUST maintain backward compatibility with Phase 1 single-sample upload endpoint

### Key Entities

- **PCAModel**: Represents fitted PCA transformation with explained_variance_ratios, n_components, mean, components (loadings)
- **Classifier**: Represents trained classifier (one-class SVM or binary) with decision_function, predict methods, hyperparameters
- **ModelMetadata**: Represents model version info with version_id, training_date, dataset_summary, performance_metrics (accuracy, ROC-AUC if applicable)
- **Batch**: Represents batch upload with batch_id, user_id, total_samples, processed_count, status (pending/processing/complete), created_at
- **PreprocessingParams**: Represents preprocessing configuration with baseline_method, filter_window, filter_order, normalization_method

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Real chemometric analysis completes in under 10 seconds for single sample (preprocessing + PCA + classification)
- **SC-002**: PCA model explains at least 95% of variance in training data
- **SC-003**: Classifier achieves at least 90% accuracy on validation set (if labeled data available)
- **SC-004**: System correctly identifies authentic samples with >85% confidence on average
- **SC-005**: Batch processing handles 50 samples in under 2 minutes
- **SC-006**: Preprocessing pipeline successfully handles 95% of uploaded spectra without errors
- **SC-007**: Model training script completes in under 5 minutes for dataset of 100 samples
- **SC-008**: Visualization endpoints return plot data in under 3 seconds
- **SC-009**: System maintains 99% uptime during Phase 2 testing period
- **SC-010**: Zero regression in Phase 1 functionality (authentication, single upload still work)

## Assumptions

1. **Training data availability**: We will use open-source spectral datasets (NIST, ChemSpider, or academic repositories) for initial model training; authentic flour/spice/herb spectra from public databases
2. **One-class classification**: Primary approach is one-class SVM trained on authentic samples only; binary classifier optional if adulterated samples available
3. **Wavelength standardization**: All spectra assumed to be in same wavelength range (e.g., 400-2500nm for NIR); resampling/interpolation handles minor variations
4. **Model storage**: Joblib format sufficient for Phase 2; cloud storage (S3) deferred to Phase 4
5. **Synchronous processing**: Single-sample analysis remains synchronous; batch processing uses asyncio.Queue with single background worker (no distributed processing)
6. **Visualization format**: JSON plot data returned; frontend rendering deferred to Phase 3
7. **Performance baseline**: Phase 2 targets local development performance; cloud optimization in Phase 4
8. **Model retraining**: Manual retraining via script; automated retraining pipeline deferred to future phases

## Dependencies

- **Phase 1 completion**: Requires fully functional authentication, database, and single-sample upload from Phase 1
- **Python ML libraries**: numpy, scipy, scikit-learn, matplotlib (add to requirements.txt)
- **Training dataset**: Requires curated authentic sample dataset (can use open-source or synthetic for MVP)
- **No external dependencies**: Self-contained; no cloud ML services (SageMaker, Azure ML) in Phase 2

## Out of Scope

The following are explicitly **not** included in Phase 2:

- Frontend dashboard or UI (Phase 3)
- Real-time model retraining or AutoML
- Distributed batch processing (Celery, RabbitMQ)
- Cloud storage for models (S3, Azure Blob)
- Advanced classifiers (neural networks, ensemble methods)
- Multi-class classification (flour vs spice vs herb)
- Anomaly detection beyond one-class SVM
- Model explainability beyond distance metrics (SHAP, LIME)
- Performance optimization (caching, GPU acceleration)
- Model A/B testing or canary deployments

## Notes

- **Model selection**: Start with one-class SVM for simplicity; can extend to binary classifier if labeled adulterated samples available
- **PCA components**: Retain components explaining 95% variance; typically 5-10 components for spectral data
- **Preprocessing order**: Baseline correction → Noise reduction → Normalization → PCA → Classification
- **Testing strategy**: Unit tests for each preprocessing step, integration tests for full pipeline, model evaluation metrics
- **Documentation**: Document model training process, hyperparameters, and performance metrics in `/models/README.md`
- **Backward compatibility**: Phase 1 endpoints must continue working; Phase 2 adds new endpoints without breaking existing ones

## Clarifications

### Session 2025-11-24
- Initial specification created based on Phase 1 completion analysis
- Prioritized real model integration (P1) over batch processing (P3) and visualization (P3)
- Assumed one-class SVM as primary classifier; binary classifier optional
- Deferred frontend visualization to Phase 3; Phase 2 returns JSON plot data only
- Q: Training dataset source for initial model? → A: Open-source spectral dataset (NIST, ChemSpider, academic repositories)
- Q: Batch processing implementation approach? → A: Simple async queue (asyncio.Queue) with single background worker
- Q: Model performance validation method? → A: Cross-validation on training set (5-fold or 10-fold)
- Q: Preprocessing parameter configuration? → A: Configuration file (YAML/JSON) with sensible defaults
- Q: Model artifact naming convention? → A: Semantic versioning with timestamp (e.g., pca_v1.0.0_20251124.joblib)
