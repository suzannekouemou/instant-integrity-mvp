"""One-class SVM classifier for authenticity detection."""
import numpy as np
from sklearn.svm import OneClassSVM
import joblib
import yaml
from pathlib import Path


def load_config():
    """Load classifier configuration from YAML."""
    config_path = Path(__file__).parent.parent.parent / "config" / "preprocessing.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def train_one_class_svm(X: np.ndarray, kernel: str = 'rbf', gamma: str = 'scale', nu: float = 0.1) -> OneClassSVM:
    """
    Train one-class SVM classifier.
    
    Args:
        X: Training data (n_samples, n_features) - authentic samples only
        kernel: Kernel type
        gamma: Kernel coefficient
        nu: Upper bound on fraction of outliers
        
    Returns:
        Trained classifier
    """
    clf = OneClassSVM(kernel=kernel, gamma=gamma, nu=nu)
    clf.fit(X)
    return clf


def predict(clf: OneClassSVM, X: np.ndarray, config: dict = None) -> tuple[str, float]:
    """
    Predict authenticity status and confidence.
    
    Args:
        clf: Trained classifier
        X: Sample to predict (n_features,) or (1, n_features)
        config: Configuration with thresholds
        
    Returns:
        Tuple of (status, confidence)
        status: 'Authentic', 'Suspect', or 'Verify'
        confidence: 0-1 score
    """
    if config is None:
        config = load_config()
    
    if X.ndim == 1:
        X = X.reshape(1, -1)
    
    # Get decision function (distance to boundary)
    decision = clf.decision_function(X)[0]
    
    # Convert to confidence score
    confidence = calculate_confidence(decision)
    
    # Determine status based on thresholds
    thresholds = config['thresholds']
    if confidence >= thresholds['authentic']:
        status = 'Authentic'
    elif confidence < thresholds['suspect']:
        status = 'Suspect'
    else:
        status = 'Verify'
    
    return status, confidence


def calculate_confidence(decision_value: float) -> float:
    """
    Convert SVM decision function to confidence score (0-1).
    
    Uses sigmoid transformation to map decision values to [0, 1].
    
    Args:
        decision_value: SVM decision function output
        
    Returns:
        Confidence score between 0 and 1
    """
    # Sigmoid transformation
    # Positive decision = authentic (closer to training data)
    # Negative decision = outlier (farther from training data)
    confidence = 1 / (1 + np.exp(-decision_value))
    return float(np.clip(confidence, 0, 1))


def load_classifier(model_path: str) -> OneClassSVM:
    """
    Load classifier from joblib file.
    
    Args:
        model_path: Path to classifier model file
        
    Returns:
        Loaded classifier
    """
    return joblib.load(model_path)
