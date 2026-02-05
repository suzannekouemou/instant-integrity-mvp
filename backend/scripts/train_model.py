"""
Training script for chemometric models.

Usage:
    python scripts/train_model.py --dataset data/training/authentic_samples.csv --version 1.0.0

Note: You need to provide training data (authentic spectral samples).
For MVP testing, you can use synthetic data or download from NIST/ChemSpider.
"""

import argparse
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ml.preprocess import preprocess_pipeline
from app.ml.features import fit_pca, get_variance_explained
from app.ml.classifier import train_one_class_svm
from app.ml.model_store import save_model


def load_training_data(csv_path: str) -> np.ndarray:
    """
    Load training data from transposed CSV format.

    Expected CSV format (olive oil FTIR spectra):
    - Row 1: Sample Numbers (1,1,2,2,3,3...)
    - Row 2: Group Codes (1,1,1,1,2,2,2...)
    - Row 3: Country labels (Greece, Greece, Italy...)
    - Row 4+: Wavenumbers as row labels (first column), then spectral values

    Returns:
        np.ndarray: Spectral data with shape (n_samples, n_features)
                    where rows are samples and columns are wavenumbers
    """
    # Read CSV with first column as index (wavenumbers)
    df = pd.read_csv(csv_path, index_col=0)

    # Skip the first 2 rows (Sample Number and Group Code)
    # Row 3 (country names) becomes the column headers after transpose
    # We need to skip rows with non-numeric data
    # The first 2 rows are "Sample Number:" and "Group Code:" which have numeric-ish data
    # The 3rd row "Wavenumbers" has country names as values

    # Drop the header rows (Sample Number, Group Code, country name row)
    # These are the first 2 rows after the index column is set
    spectral_df = df.iloc[2:]  # Skip "Sample Number:", "Group Code:" rows

    # Convert to numeric (country names in row 3 were already skipped by iloc[2:])
    # The remaining data should be numeric spectral values
    spectral_df = spectral_df.apply(pd.to_numeric, errors="coerce")

    # Transpose so rows become samples and columns become wavenumbers (features)
    spectral_df = spectral_df.T

    # Drop any rows with NaN values (shouldn't be any if data is clean)
    spectral_df = spectral_df.dropna()

    return spectral_df.values


def main():
    parser = argparse.ArgumentParser(description="Train chemometric models")
    parser.add_argument("--dataset", required=True, help="Path to training CSV")
    parser.add_argument("--version", default="1.0.0", help="Model version (semantic)")
    args = parser.parse_args()

    print(f"Loading training data from {args.dataset}...")
    X_raw = load_training_data(args.dataset)

    print(f"Loaded {X_raw.shape[0]} samples with {X_raw.shape[1]} features")

    # Preprocess all samples
    print("Preprocessing spectra...")
    X_preprocessed = np.array([preprocess_pipeline(x)[0] for x in X_raw])

    # Fit PCA
    print("Fitting PCA model...")
    pca = fit_pca(X_preprocessed, variance_threshold=0.95)
    variance_explained = get_variance_explained(pca)
    print(
        f"PCA: {pca.n_components_} components, {variance_explained:.2%} variance explained"
    )

    # Transform to PCA space
    X_pca = pca.transform(X_preprocessed)

    # Train classifier
    print("Training one-class SVM...")
    clf = train_one_class_svm(X_pca, kernel="rbf", gamma="scale", nu=0.1)

    # Evaluate model on training data (for one-class SVM)
    # One-class SVM doesn't support standard CV, so we evaluate on training set
    print("Evaluating model...")
    predictions = clf.predict(X_pca)
    # OneClassSVM returns 1 for inliers, -1 for outliers
    inlier_ratio = (predictions == 1).sum() / len(predictions)
    print(f"Training set inlier ratio: {inlier_ratio:.2%}")

    # Use decision function scores for additional metrics
    decision_scores = clf.decision_function(X_pca)
    print(
        f"Decision score mean: {decision_scores.mean():.4f}, std: {decision_scores.std():.4f}"
    )

    # Save models
    print(f"Saving models (version {args.version})...")

    pca_metadata = {
        "dataset_summary": {
            "source": args.dataset,
            "num_samples": X_raw.shape[0],
            "wavelength_range": [400, 2500],  # Adjust based on your data
        },
        "pca_metrics": {
            "n_components": int(pca.n_components_),
            "variance_explained": float(variance_explained),
            "explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        },
    }

    clf_metadata = {
        "classifier_metrics": {
            "inlier_ratio": float(inlier_ratio),
            "decision_score_mean": float(decision_scores.mean()),
            "decision_score_std": float(decision_scores.std()),
            "kernel": "rbf",
            "gamma": "scale",
            "nu": 0.1,
        }
    }

    pca_path, pca_meta_path = save_model(pca, "pca", args.version, pca_metadata)
    clf_path, clf_meta_path = save_model(clf, "classifier", args.version, clf_metadata)

    print(f"\n✅ Training complete!")
    print(f"PCA model: {pca_path}")
    print(f"Classifier model: {clf_path}")
    print(f"Metadata: {pca_meta_path}")


if __name__ == "__main__":
    main()
