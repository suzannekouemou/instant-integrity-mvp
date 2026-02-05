"""PCA feature extraction for spectral data."""
import numpy as np
from sklearn.decomposition import PCA
import joblib
from pathlib import Path


def fit_pca(X: np.ndarray, variance_threshold: float = 0.95) -> PCA:
    """
    Fit PCA model on training data.
    
    Args:
        X: Training data (n_samples, n_features)
        variance_threshold: Retain components explaining this much variance
        
    Returns:
        Fitted PCA model
    """
    pca = PCA(n_components=variance_threshold, svd_solver='full')
    pca.fit(X)
    return pca


def transform_pca(pca: PCA, X: np.ndarray) -> np.ndarray:
    """
    Transform spectra using fitted PCA model.
    
    Args:
        pca: Fitted PCA model
        X: Spectra to transform (n_samples, n_features) or (n_features,)
        
    Returns:
        PCA-transformed data
    """
    if X.ndim == 1:
        X = X.reshape(1, -1)
    return pca.transform(X)


def load_pca_model(model_path: str) -> PCA:
    """
    Load PCA model from joblib file.
    
    Args:
        model_path: Path to PCA model file
        
    Returns:
        Loaded PCA model
    """
    return joblib.load(model_path)


def get_variance_explained(pca: PCA) -> float:
    """
    Get total variance explained by PCA model.
    
    Args:
        pca: Fitted PCA model
        
    Returns:
        Total variance explained (0-1)
    """
    return float(np.sum(pca.explained_variance_ratio_))
