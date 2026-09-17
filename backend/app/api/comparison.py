from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.comparison_service import AdmissionService
from app.schemas.comparison import AdmissionCreate, AdmissionUpdate, AdmissionResponse, AdmissionListResponse

router = APIRouter(prefix="/admissions", tags=["Admissions"])


@router.post("", response_model=AdmissionResponse, status_code=201)
async def create_admission(admission_data: AdmissionCreate, db: Session = Depends(get_db)):
    service = AdmissionService(db)
    return service.create(admission_data)


@router.get("", response_model=AdmissionListResponse)
async def list_admissions(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    university_id: Optional[str] = Query(None),
    programme_id: Optional[str] = Query(None),
    academic_year: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    service = AdmissionService(db)
    return service.get_all(page, size, search, status, university_id, programme_id, academic_year, is_active)


@router.get("/open", response_model=list[AdmissionResponse])
async def get_open_admissions(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    service = AdmissionService(db)
    return service.get_open_admissions(limit)


@router.get("/{admission_id}", response_model=AdmissionResponse)
async def get_admission(admission_id: str, db: Session = Depends(get_db)):
    service = AdmissionService(db)
    return service.get_by_id(admission_id)


@router.put("/{admission_id}", response_model=AdmissionResponse)
async def update_admission(
    admission_id: str,
    admission_data: AdmissionUpdate,
    db: Session = Depends(get_db),
):
    service = AdmissionService(db)
    return service.update(admission_id, admission_data)


@router.delete("/{admission_id}", status_code=204)
async def delete_admission(admission_id: str, db: Session = Depends(get_db)):
    service = AdmissionService(db)
    service.delete(admission_id)
    return None