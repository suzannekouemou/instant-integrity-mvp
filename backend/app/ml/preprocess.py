"""Spectral data preprocessing pipeline."""
import numpy as np
from scipy import sparse
from scipy.signal import savgol_filter
from scipy.linalg import cholesky
import yaml
from pathlib import Path


def load_config():
    """Load preprocessing configuration from YAML."""
    config_path = Path(__file__).parent.parent.parent / "config" / "preprocessing.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def baseline_als(spectra: np.ndarray, lam: float = 1e5, p: float = 0.01, niter: int = 10) -> np.ndarray:
    """
    Asymmetric Least Squares baseline correction.
    
    Args:
        spectra: 1D array of spectral intensities
        lam: Smoothness parameter (larger = smoother baseline)
        p: Asymmetry parameter (0 < p < 1, smaller = more asymmetric)
        niter: Number of iterations
        
    Returns:
        Baseline-corrected spectra
    """
    L = len(spectra)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L-2))
    D = lam * D.dot(D.transpose())
    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)
    
    for _ in range(niter):
        W.setdiag(w)
        Z = W + D
        z = sparse.linalg.spsolve(Z, w * spectra)
        w = p * (spectra > z) + (1 - p) * (spectra < z)
    
    return spectra - z


def baseline_polynomial(spectra: np.ndarray, degree: int = 3) -> np.ndarray:
    """
    Polynomial baseline correction.
    
    Args:
        spectra: 1D array of spectral intensities
        degree: Polynomial degree
        
    Returns:
        Baseline-corrected spectra
    """
    x = np.arange(len(spectra))
    coeffs = np.polyfit(x, spectra, degree)
    baseline = np.polyval(coeffs, x)
    return spectra - baseline


def savgol_filter_wrapper(spectra: np.ndarray, window_size: int = 11, poly_order: int = 3) -> np.ndarray:
    """
    Savitzky-Golay filter for noise reduction.
    
    Args:
        spectra: 1D array of spectral intensities
        window_size: Window size (must be odd)
        poly_order: Polynomial order
        
    Returns:
        Smoothed spectra
    """
    if window_size % 2 == 0:
        window_size += 1  # Ensure odd
    return savgol_filter(spectra, window_size, poly_order)


def normalize_snv(spectra: np.ndarray) -> np.ndarray:
    """
    Standard Normal Variate (SNV) normalization.
    
    Args:
        spectra: 1D array of spectral intensities
        
    Returns:
        SNV-normalized spectra
    """
    mean = np.mean(spectra)
    std = np.std(spectra)
    if std == 0:
        return spectra - mean
    return (spectra - mean) / std


def normalize_mean_center(spectra: np.ndarray, reference_mean: float = None) -> np.ndarray:
    """
    Mean-centering normalization.
    
    Args:
        spectra: 1D array of spectral intensities
        reference_mean: Reference mean (if None, uses spectra mean)
        
    Returns:
        Mean-centered spectra
    """
    if reference_mean is None:
        reference_mean = np.mean(spectra)
    return spectra - reference_mean


def preprocess_pipeline(spectra: np.ndarray, config: dict = None) -> tuple[np.ndarray, dict]:
    """
    Complete preprocessing pipeline.
    
    Args:
        spectra: 1D array of spectral intensities
        config: Preprocessing configuration (if None, loads from YAML)
        
    Returns:
        Tuple of (preprocessed_spectra, preprocessing_params)
    """
    if config is None:
        config = load_config()
    
    params = {}
    result = spectra.copy()
    
    # Baseline correction
    baseline_method = config['baseline']['method']
    params['baseline_method'] = baseline_method
    
    if baseline_method == 'als':
        result = baseline_als(
            result,
            lam=config['baseline']['als_lambda'],
            p=config['baseline']['als_p']
        )
        params['als_lambda'] = config['baseline']['als_lambda']
        params['als_p'] = config['baseline']['als_p']
    elif baseline_method == 'polynomial':
        result = baseline_polynomial(result, degree=config['baseline']['polynomial_degree'])
        params['polynomial_degree'] = config['baseline']['polynomial_degree']
    
    # Noise reduction
    if config['noise_reduction']['method'] == 'savgol':
        result = savgol_filter_wrapper(
            result,
            window_size=config['noise_reduction']['window_size'],
            poly_order=config['noise_reduction']['polynomial_order']
        )
        params['filter_window'] = config['noise_reduction']['window_size']
        params['filter_order'] = config['noise_reduction']['polynomial_order']
    
    # Normalization
    norm_method = config['normalization']['method']
    params['normalization'] = norm_method
    
    if norm_method == 'snv':
        result = normalize_snv(result)
    elif norm_method == 'mean_center':
        result = normalize_mean_center(result)
    
    return result, params
