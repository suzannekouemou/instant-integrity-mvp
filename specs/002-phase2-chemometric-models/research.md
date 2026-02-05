# Research & Technology Decisions: Phase 2

**Feature**: Phase 2 - Chemometric Model Integration  
**Date**: 2025-11-24

## Overview

This document captures research findings and technology decisions for implementing real chemometric analysis in Phase 2.

---

## 1. Training Dataset Sources

### Decision
Use **NIST Chemistry WebBook** and **ChemSpider** for open-source spectral data

### Rationale
- **Free access**: Both provide free spectral data downloads
- **Quality**: NIST is gold standard for reference spectra
- **Coverage**: Both cover flour, spice, herb categories
- **Format**: Standard JCAMP-DX format, easily parseable
- **Volume**: Sufficient samples for initial training (100+ per category)

### Alternatives Considered
- **Synthetic data**: Rejected - less realistic, doesn't capture real-world variability
- **Partner/client data**: Rejected - requires data sharing agreements, delays Phase 2
- **New sample collection**: Rejected - expensive, time-consuming

### Implementation Notes
- NIST: Download via Chemistry WebBook API (free, no rate limits)
- ChemSpider: Use free tier API (1000 requests/day sufficient)
- Store raw spectra in `/data/training/` directory
- Document data sources in `models/README.md`

---

## 2. Baseline Correction Methods

### Decision
**Asymmetric Least Squares (ALS)** as default, **polynomial fitting** as fallback

### Rationale
- **ALS advantages**: Handles fluorescence background better, adaptive to baseline shape
- **Polynomial advantages**: Simpler, faster, works well for clean spectra
- **Flexibility**: Config file allows switching based on sample type

### Alternatives Considered
- **Wavelet transform**: Rejected - too complex for Phase 2, requires additional dependencies
- **Rubberband correction**: Rejected - less effective for spectral data

### Implementation Notes
```python
# ALS parameters (config/preprocessing.yaml)
als_lambda: 1e5  # Smoothness parameter
als_p: 0.01      # Asymmetry parameter

# Polynomial parameters
polynomial_degree: 3  # Cubic polynomial
```

### References
- Eilers & Boelens (2005): "Baseline Correction with Asymmetric Least Squares Smoothing"
- scipy.signal.savgol_filter documentation

---

## 3. Noise Reduction: Savitzky-Golay Filter

### Decision
**Window size 11, polynomial order 3** (configurable via YAML)

### Rationale
- **Standard practice**: Widely used in spectroscopy for smoothing
- **Preserves peaks**: Unlike moving average, maintains peak shape
- **Configurable**: Can adjust for different noise levels

### Alternatives Considered
- **Moving average**: Rejected - loses peak shape, over-smooths
- **Gaussian filter**: Rejected - requires sigma tuning, less standard
- **Median filter**: Rejected - not suitable for continuous spectral data

### Implementation Notes
```python
from scipy.signal import savgol_filter

# Apply filter
smoothed = savgol_filter(
    spectra, 
    window_length=11,  # Must be odd
    polyorder=3
)
```

### References
- Savitzky & Golay (1964): "Smoothing and Differentiation of Data by Simplified Least Squares Procedures"

---

## 4. Normalization Methods

### Decision
**Standard Normal Variate (SNV)** as default, **mean-centering** as alternative

### Rationale
- **SNV**: Removes multiplicative scatter effects, standard in NIR spectroscopy
- **Mean-centering**: Simpler, works well for PCA preprocessing
- **Sample-specific**: SNV applied per sample, mean-centering across dataset

### Alternatives Considered
- **Min-max scaling**: Rejected - sensitive to outliers
- **Unit vector normalization**: Rejected - less interpretable for spectral data

### Implementation Notes
```python
# SNV normalization
def normalize_snv(spectra):
    mean = np.mean(spectra)
    std = np.std(spectra)
    return (spectra - mean) / std

# Mean-centering
def normalize_mean_center(spectra, reference_mean):
    return spectra - reference_mean
```

---

## 5. PCA Configuration

### Decision
Retain components explaining **95% of variance**

### Rationale
- **Industry standard**: 95% is common threshold in chemometrics
- **Dimensionality reduction**: Typically reduces to 5-10 components for spectral data
- **Overfitting prevention**: Discarding low-variance components reduces noise

### Alternatives Considered
- **Fixed number of components**: Rejected - not adaptive to data complexity
- **99% variance**: Rejected - may include noise components
- **Scree plot manual selection**: Rejected - not automatable

### Implementation Notes
```python
from sklearn.decomposition import PCA

pca = PCA(n_components=0.95)  # Retain 95% variance
pca.fit(preprocessed_spectra)

# Typically results in 5-10 components
print(f"Components retained: {pca.n_components_}")
print(f"Variance explained: {pca.explained_variance_ratio_}")
```

---

## 6. Classifier Selection: One-Class SVM

### Decision
**One-class SVM with RBF kernel**, gamma='scale'

### Rationale
- **One-class approach**: Only authentic samples needed for training
- **RBF kernel**: Handles non-linear decision boundaries in spectral space
- **Auto-scaling**: gamma='scale' adapts to feature dimensionality
- **Proven**: Standard for novelty detection in chemometrics

### Alternatives Considered
- **Isolation Forest**: Rejected - less interpretable, no distance metric
- **Local Outlier Factor**: Rejected - requires more samples, slower
- **Binary classifier**: Deferred - requires adulterated samples (Phase 3)

### Implementation Notes
```python
from sklearn.svm import OneClassSVM

clf = OneClassSVM(
    kernel='rbf',
    gamma='scale',  # 1 / (n_features * X.var())
    nu=0.1          # Upper bound on fraction of outliers
)
clf.fit(pca_transformed_authentic_samples)

# Prediction
decision = clf.decision_function(new_sample)  # Distance to boundary
prediction = clf.predict(new_sample)          # +1 (authentic) or -1 (outlier)
```

### References
- Schölkopf et al. (2001): "Estimating the Support of a High-Dimensional Distribution"

---

## 7. Batch Processing Architecture

### Decision
**asyncio.Queue with single background worker**

### Rationale
- **Simplicity**: No external dependencies (Redis, RabbitMQ)
- **Sufficient**: Handles 50 samples easily in <2 minutes
- **Async**: Non-blocking API responses
- **Upgradeable**: Can migrate to Celery in Phase 4 if needed

### Alternatives Considered
- **Celery + RabbitMQ**: Rejected - overkill for Phase 2, adds infrastructure complexity
- **Redis queue**: Rejected - unnecessary for single-worker scenario
- **Synchronous processing**: Rejected - blocks API, poor UX

### Implementation Notes
```python
import asyncio

# Global queue
batch_queue = asyncio.Queue()

# Background worker
async def batch_worker():
    while True:
        batch_id, samples = await batch_queue.get()
        for sample in samples:
            result = await process_sample(sample)
            await update_batch_progress(batch_id, result)
        batch_queue.task_done()

# Start worker on app startup
@app.on_event("startup")
async def start_batch_worker():
    asyncio.create_task(batch_worker())
```

---

## 8. Model Versioning Strategy

### Decision
**Semantic versioning + timestamp**: `pca_v1.0.0_20251124.joblib`

### Rationale
- **Semantic versioning**: MAJOR.MINOR.PATCH indicates breaking changes
- **Timestamp**: Ensures uniqueness, easy to identify latest
- **Human-readable**: Clear version progression
- **Rollback-friendly**: Easy to revert to previous version

### Alternatives Considered
- **Git commit hash**: Rejected - not human-readable, requires Git context
- **Incremental numbers**: Rejected - no semantic meaning
- **Date-only**: Rejected - no indication of breaking changes

### Implementation Notes
```python
# Model naming convention
def get_model_filename(model_type, version, date):
    return f"{model_type}_v{version}_{date}.joblib"

# Example
pca_file = get_model_filename("pca", "1.0.0", "20251124")
# Result: pca_v1.0.0_20251124.joblib

# Metadata file
metadata_file = f"metadata_v{version}_{date}.json"
```

### Versioning Rules
- **MAJOR**: Breaking changes (e.g., different PCA components, new preprocessing)
- **MINOR**: Backward-compatible improvements (e.g., better hyperparameters)
- **PATCH**: Bug fixes, no model retraining

---

## 9. Cross-Validation Approach

### Decision
**5-fold stratified cross-validation**

### Rationale
- **Bias-variance balance**: 5 folds is standard for small-medium datasets
- **Stratified**: Maintains class distribution in each fold (if applicable)
- **Computational efficiency**: Faster than 10-fold, minimal accuracy difference

### Alternatives Considered
- **10-fold CV**: Rejected - slower, minimal accuracy gain for one-class SVM
- **Leave-one-out CV**: Rejected - too slow for 100+ samples
- **Bootstrap**: Rejected - more complex, less standard

### Implementation Notes
```python
from sklearn.model_selection import cross_val_score

# One-class SVM cross-validation
scores = cross_val_score(
    clf, 
    X_train, 
    cv=5,  # 5-fold
    scoring='accuracy'  # Or custom scorer for one-class
)

print(f"CV Accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")
```

---

## 10. Configuration Management

### Decision
**YAML configuration file** with sensible defaults

### Rationale
- **Human-readable**: Easy to edit without code changes
- **Version-controllable**: Track parameter changes in Git
- **Flexible**: Override defaults per sample_type if needed
- **Standard**: PyYAML widely used, no custom parsing

### Alternatives Considered
- **Hardcoded parameters**: Rejected - requires code changes for tuning
- **Database-stored**: Rejected - overkill for Phase 2, adds complexity
- **Environment variables**: Rejected - too many parameters, not structured

### Implementation Notes
```yaml
# config/preprocessing.yaml
baseline:
  method: als
  als_lambda: 1e5
  als_p: 0.01

noise_reduction:
  method: savgol
  window_size: 11
  polynomial_order: 3

normalization:
  method: snv

wavelength:
  min: 400
  max: 2500
  tolerance: 5
```

```python
import yaml

def load_preprocessing_config():
    with open('config/preprocessing.yaml') as f:
        return yaml.safe_load(f)
```

---

## Summary

All technology decisions finalized:
- ✅ Training data: NIST + ChemSpider
- ✅ Preprocessing: ALS baseline, Savitzky-Golay filter, SNV normalization
- ✅ PCA: 95% variance threshold
- ✅ Classifier: One-class SVM with RBF kernel
- ✅ Batch processing: asyncio.Queue
- ✅ Model versioning: Semantic + timestamp
- ✅ Validation: 5-fold cross-validation
- ✅ Configuration: YAML files

**Status**: Ready for data model and API contract design
