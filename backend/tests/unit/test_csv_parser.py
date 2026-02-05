import pytest
from pathlib import Path
from app.utils.csv_parser import validate_csv


def test_valid_csv():
    """Test validation of valid CSV file."""
    csv_content = "wavelength,absorbance\n400.0,0.123\n450.0,0.145\n"
    is_valid, error, data = validate_csv(csv_content)
    
    assert is_valid is True
    assert error == ""
    assert data is not None
    assert len(data) == 2
    assert data[0]['wavelength'] == 400.0
    assert data[0]['absorbance'] == 0.123


def test_invalid_columns():
    """Test CSV with wrong columns."""
    csv_content = "wrong,columns\n400.0,0.123\n"
    is_valid, error, data = validate_csv(csv_content)
    
    assert is_valid is False
    assert "wavelength" in error.lower() or "absorbance" in error.lower()
    assert data is None


def test_empty_csv():
    """Test empty CSV file."""
    csv_content = "wavelength,absorbance\n"
    is_valid, error, data = validate_csv(csv_content)
    
    assert is_valid is False
    assert "empty" in error.lower()


def test_invalid_data_types():
    """Test CSV with invalid data types."""
    csv_content = "wavelength,absorbance\ninvalid,0.123\n"
    is_valid, error, data = validate_csv(csv_content)
    
    assert is_valid is False
    assert data is None
