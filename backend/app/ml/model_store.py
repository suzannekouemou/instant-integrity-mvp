"""Model storage and versioning utilities."""
import joblib
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


def get_model_dir() -> Path:
    """Get models directory path."""
    return Path(__file__).parent.parent.parent / "models"


def generate_model_filename(model_type: str, version: str, date: str = None) -> str:
    """
    Generate model filename with semantic versioning and timestamp.
    
    Args:
        model_type: Type of model ('pca', 'classifier')
        version: Semantic version (e.g., '1.0.0')
        date: Date string (YYYYMMDD), defaults to today
        
    Returns:
        Filename string
    """
    if date is None:
        date = datetime.now().strftime('%Y%m%d')
    return f"{model_type}_v{version}_{date}.joblib"


def save_model(model: Any, model_type: str, version: str, metadata: Dict[str, Any] = None) -> tuple[str, str]:
    """
    Save model and metadata to disk.
    
    Args:
        model: Model object to save
        model_type: Type of model ('pca', 'classifier')
        version: Semantic version
        metadata: Optional metadata dictionary
        
    Returns:
        Tuple of (model_path, metadata_path)
    """
    model_dir = get_model_dir()
    model_dir.mkdir(exist_ok=True)
    
    date = datetime.now().strftime('%Y%m%d')
    model_filename = generate_model_filename(model_type, version, date)
    model_path = model_dir / model_filename
    
    # Save model
    joblib.dump(model, model_path)
    
    # Save metadata if provided
    metadata_path = None
    if metadata:
        metadata_filename = f"metadata_v{version}_{date}.json"
        metadata_path = model_dir / metadata_filename
        
        # Add model filename to metadata
        metadata[f'{model_type}_model'] = model_filename
        metadata['version'] = version
        metadata['training_date'] = date
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    return str(model_path), str(metadata_path) if metadata_path else None


def load_latest_model(model_type: str) -> Optional[Any]:
    """
    Load the latest version of a model by timestamp.
    
    Args:
        model_type: Type of model ('pca', 'classifier')
        
    Returns:
        Loaded model or None if not found
    """
    model_dir = get_model_dir()
    
    # Find all model files of this type
    pattern = f"{model_type}_v*.joblib"
    model_files = list(model_dir.glob(pattern))
    
    if not model_files:
        return None
    
    # Sort by filename (version and date) and get latest
    latest_file = sorted(model_files)[-1]
    return joblib.load(latest_file)


def list_model_versions(model_type: str = None) -> list[Dict[str, Any]]:
    """
    List all available model versions.
    
    Args:
        model_type: Optional filter by model type
        
    Returns:
        List of model info dictionaries
    """
    model_dir = get_model_dir()
    
    if model_type:
        pattern = f"{model_type}_v*.joblib"
    else:
        pattern = "*_v*.joblib"
    
    model_files = list(model_dir.glob(pattern))
    
    models = []
    for model_file in sorted(model_files):
        # Parse filename: {type}_v{version}_{date}.joblib
        parts = model_file.stem.split('_v')
        if len(parts) == 2:
            mtype = parts[0]
            version_date = parts[1].split('_')
            if len(version_date) == 2:
                version, date = version_date
                
                # Try to load corresponding metadata
                metadata_file = model_dir / f"metadata_v{version}_{date}.json"
                metadata = {}
                if metadata_file.exists():
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                
                models.append({
                    'model_type': mtype,
                    'version': version,
                    'date': date,
                    'filename': model_file.name,
                    'metadata': metadata
                })
    
    return models


def get_model_metadata(version: str, date: str) -> Optional[Dict[str, Any]]:
    """
    Load metadata for a specific model version.
    
    Args:
        version: Model version
        date: Model date (YYYYMMDD)
        
    Returns:
        Metadata dictionary or None
    """
    model_dir = get_model_dir()
    metadata_file = model_dir / f"metadata_v{version}_{date}.json"
    
    if not metadata_file.exists():
        return None
    
    with open(metadata_file) as f:
        return json.load(f)
