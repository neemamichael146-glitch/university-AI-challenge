from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.university_service import UniversityService
from app.schemas.university import UniversityCreate, UniversityUpdate, UniversityResponse, UniversityListResponse

router = APIRouter(prefix="/universities", tags=["Universities"])


@router.post("", response_model=UniversityResponse, status_code=201)
async def create_university(university_data: UniversityCreate, db: Session = Depends(get_db)):
    service = UniversityService(db)
    return service.create(university_data)


@router.get("", response_model=UniversityListResponse)
async def list_universities(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    is_public: Optional[bool] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    service = UniversityService(db)
    return service.get_all(page, size, search, region, is_public, is_active)


@router.get("/regions", response_model=list[str])
async def get_regions(db: Session = Depends(get_db)):
    service = UniversityService(db)
    return service.get_regions()


@router.get("/{university_id}", response_model=UniversityResponse)
async def get_university(university_id: str, db: Session = Depends(get_db)):
    service = UniversityService(db)
    return service.get_by_id(university_id)


@router.put("/{university_id}", response_model=UniversityResponse)
async def update_university(
    university_id: str,
    university_data: UniversityUpdate,
    db: Session = Depends(get_db),
):
    service = UniversityService(db)
    return service.update(university_id, university_data)


@router.delete("/{university_id}", status_code=204)
async def delete_university(university_id: str, db: Session = Depends(get_db)):
    service = UniversityService(db)
    service.delete(university_id)
    return None