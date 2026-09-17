from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.programme_service import ProgrammeService
from app.schemas.programmes import ProgrammeCreate, ProgrammeUpdate, ProgrammeResponse, ProgrammeListResponse

router = APIRouter(prefix="/programmes", tags=["Programmes"])


@router.post("", response_model=ProgrammeResponse, status_code=201)
async def create_programme(programme_data: ProgrammeCreate, db: Session = Depends(get_db)):
    service = ProgrammeService(db)
    return service.create(programme_data)


@router.get("", response_model=ProgrammeListResponse)
async def list_programmes(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    university_id: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_featured: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    service = ProgrammeService(db)
    return service.get_all(page, size, search, level, university_id, is_active, is_featured)


@router.get("/levels", response_model=list[str])
async def get_levels():
    service = ProgrammeService(None)
    return service.get_levels()


@router.get("/{programme_id}", response_model=ProgrammeResponse)
async def get_programme(programme_id: str, db: Session = Depends(get_db)):
    service = ProgrammeService(db)
    return service.get_by_id(programme_id)


@router.put("/{programme_id}", response_model=ProgrammeResponse)
async def update_programme(
    programme_id: str,
    programme_data: ProgrammeUpdate,
    db: Session = Depends(get_db),
):
    service = ProgrammeService(db)
    return service.update(programme_id, programme_data)


@router.delete("/{programme_id}", status_code=204)
async def delete_programme(programme_id: str, db: Session = Depends(get_db)):
    service = ProgrammeService(db)
    service.delete(programme_id)
    return None