# Model Artifacts Directory

This directory stores trained chemometric models for authenticity analysis.

## Model Versioning Convention

Models follow semantic versioning with timestamps:

```
{model_type}_v{MAJOR}.{MINOR}.{PATCH}_{YYYYMMDD}.joblib
```

**Examples**:
- `pca_v1.0.0_20251124.joblib`
- `classifier_v1.0.0_20251124.joblib`

## Versioning Rules

- **MAJOR**: Breaking changes (e.g., different number of PCA components, new preprocessing method)
- **MINOR**: Backward-compatible improvements (e.g., better hyperparameters, more training data)
- **PATCH**: Bug fixes, no model retraining required

## Model Files

Each model version consists of:

1. **PCA Model** (`pca_v*.joblib`): Fitted PCA transformation
2. **Classifier Model** (`classifier_v*.joblib`): Trained one-class SVM
3. **Metadata** (`metadata_v*.json`): Training info, metrics, hyperparameters

## Metadata Schema

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
    "variance_explained": 0.96
  },
  "classifier_metrics": {
    "cv_accuracy": 0.91,
    "cv_std": 0.03
  }
}
```

## Training New Models

Run the training script:

```bash
cd backend
python scripts/train_model.py --dataset data/training/authentic_samples.csv --version 1.1.0
```

## Loading Models

Models are automatically loaded on application startup. The system loads the latest version based on timestamp.

```python
from app.ml.model_store import load_latest_model

pca_model = load_latest_model("pca")
classifier_model = load_latest_model("classifier")
```
