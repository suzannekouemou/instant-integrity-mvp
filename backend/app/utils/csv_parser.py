import csv
from io import StringIO


def validate_csv(content: str) -> tuple[bool, str, list[dict] | None]:
    """
    Validate CSV spectral data format.
    
    Returns:
        (is_valid, error_message, parsed_data)
    """
    try:
        reader = csv.DictReader(StringIO(content))
        rows = list(reader)
        
        if not rows:
            return False, "CSV file is empty", None
        
        # Check required columns
        if 'wavelength' not in reader.fieldnames or 'absorbance' not in reader.fieldnames:
            return False, "CSV must contain 'wavelength' and 'absorbance' columns", None
        
        # Validate data types and ranges
        parsed_data = []
        for i, row in enumerate(rows):
            try:
                wavelength = float(row['wavelength'])
                absorbance = float(row['absorbance'])
                
                if wavelength < 0 or wavelength > 10000:
                    return False, f"Invalid wavelength at row {i+1}: {wavelength}", None
                
                parsed_data.append({
                    'wavelength': wavelength,
                    'absorbance': absorbance
                })
            except (ValueError, KeyError) as e:
                return False, f"Invalid data at row {i+1}: {str(e)}", None
        
        return True, "", parsed_data
        
    except Exception as e:
        return False, f"CSV parsing error: {str(e)}", None
