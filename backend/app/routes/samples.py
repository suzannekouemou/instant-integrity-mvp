from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.core.rate_limit import limiter
from app.models.user import User
from app.models.sample import Sample
from app.schemas.sample import SampleType, SampleResponse
from app.schemas.result import ResultResponse
from app.utils.csv_parser import validate_csv
from app.services.analysis_service import analyze_sample

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def rate_limit_decorator(limit_string: str):
    """Return rate limit decorator if limiter is enabled, else passthrough."""
    if limiter:
        return limiter.limit(limit_string)
    return lambda func: func


@router.post(
    "/upload", response_model=ResultResponse, status_code=status.HTTP_201_CREATED
)
@rate_limit_decorator("10/hour")
async def upload_sample(
    request: Request,
    file: UploadFile = File(...),
    sample_type: SampleType = Form(...),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Upload CSV spectral data and receive real authenticity analysis."""
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV files are allowed"
        )

    # Read file content
    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum of {MAX_FILE_SIZE / 1024 / 1024}MB",
        )

    # Decode and validate CSV
    try:
        csv_content = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File must be UTF-8 encoded"
        )

    is_valid, error, parsed_data = validate_csv(csv_content)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    # Store sample
    sample = Sample(
        user_id=current_user.id,
        filename=file.filename,
        sample_type=sample_type.value,
        spectra_points={"data": parsed_data},
        sample_metadata={"original_filename": file.filename, "file_size": len(content)},
    )
    db.add(sample)
    await db.flush()

    # Convert parsed data to numpy array for analysis
    # parsed_data is list of dicts like [{'wavelength': x, 'absorbance': y}, ...]
    # Extract just the absorbance values for the spectral analysis
    spectra = np.array([point["absorbance"] for point in parsed_data], dtype=float)

    # Analyze with real chemometric pipeline
    result = await analyze_sample(db, sample.id, spectra)

    return result
