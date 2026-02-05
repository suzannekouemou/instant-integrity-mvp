from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.result import Result
from app.models.sample import Sample
from app.schemas.result import ResultResponse

router = APIRouter()


@router.get("/{sample_id}", response_model=ResultResponse)
async def get_result(
    sample_id: UUID,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Retrieve analysis result for a sample."""
    # Get sample to check ownership
    sample_result = await db.execute(
        select(Sample).where(Sample.id == sample_id)
    )
    sample = sample_result.scalar_one_or_none()
    
    if not sample:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sample not found"
        )
    
    # Check authorization
    if sample.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this sample"
        )
    
    # Get result
    result_query = await db.execute(
        select(Result).where(Result.sample_id == sample_id)
    )
    result = result_query.scalar_one_or_none()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found for this sample"
        )
    
    return result
