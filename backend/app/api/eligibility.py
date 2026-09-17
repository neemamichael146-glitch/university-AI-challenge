from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.eligibility_service import ScholarshipService
from app.schemas.eligibility import (
    ScholarshipCreate, ScholarshipUpdate, ScholarshipResponse, ScholarshipListResponse,
    EligibilityCheckRequest, EligibilityResult, EligibilityComparison
)

router = APIRouter(prefix="/scholarships", tags=["Scholarships"])


@router.post("", response_model=ScholarshipResponse, status_code=201)
async def create_scholarship(scholarship_data: ScholarshipCreate, db: Session = Depends(get_db)):
    service = ScholarshipService(db)
    return service.create(scholarship_data)


@router.get("", response_model=ScholarshipListResponse)
async def list_scholarships(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    university_id: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_featured: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    service = ScholarshipService(db)
    return service.get_all(page, size, search, type, university_id, is_active, is_featured)


@router.get("/types", response_model=list[str])
async def get_scholarship_types():
    service = ScholarshipService(None)
    return service.get_types()


@router.get("/{scholarship_id}", response_model=ScholarshipResponse)
async def get_scholarship(scholarship_id: str, db: Session = Depends(get_db)):
    service = ScholarshipService(db)
    return service.get_by_id(scholarship_id)


@router.put("/{scholarship_id}", response_model=ScholarshipResponse)
async def update_scholarship(
    scholarship_id: str,
    scholarship_data: ScholarshipUpdate,
    db: Session = Depends(get_db),
):
    service = ScholarshipService(db)
    return service.update(scholarship_id, scholarship_data)


@router.delete("/{scholarship_id}", status_code=204)
async def delete_scholarship(scholarship_id: str, db: Session = Depends(get_db)):
    service = ScholarshipService(db)
    service.delete(scholarship_id)
    return None


@router.post("/check-eligibility", response_model=EligibilityResult)
async def check_eligibility(request: EligibilityCheckRequest, db: Session = Depends(get_db)):
    return EligibilityResult(
        is_eligible=True,
        score=85.0,
        requirements_met=["Direct entry qualifications"],
        requirements_missing=["Specific subject requirements"],
        recommendations=["Check specific subject requirements"],
        programme_requirements={},
    )


@router.post("/compare-eligibility", response_model=list[EligibilityComparison])
async def compare_eligibility(request: EligibilityCheckRequest, db: Session = Depends(get_db)):
    return [
        EligibilityComparison(
            programme_id=request.programme_id,
            programme_name="Sample Programme",
            is_eligible=True,
            score=85.0,
            missing_requirements=[],
        )
    ]