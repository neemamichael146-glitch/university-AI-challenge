from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.core.exceptions import NotFoundException, ValidationException
from app.models.university import University
from app.schemas.university import UniversityCreate, UniversityUpdate


class UniversityService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, university_data: UniversityCreate) -> University:
        existing = self.db.query(University).filter(
            or_(University.name == university_data.name, University.short_name == university_data.short_name)
        ).first()
        if existing:
            raise ConflictException("University with this name or short name already exists")

        university = University(**university_data.model_dump())
        self.db.add(university)
        self.db.commit()
        self.db.refresh(university)
        return university

    def get_by_id(self, university_id: str) -> University:
        university = self.db.query(University).filter(University.id == university_id).first()
        if not university:
            raise NotFoundException("University", university_id)
        return university

    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        search: Optional[str] = None,
        region: Optional[str] = None,
        is_public: Optional[bool] = None,
        is_active: Optional[bool] = None,
    ) -> Dict[str, Any]:
        query = self.db.query(University)

        if search:
            query = query.filter(
                or_(
                    University.name.ilike(f"%{search}%"),
                    University.short_name.ilike(f"%{search}%"),
                    University.city.ilike(f"%{search}%"),
                )
            )

        if region:
            query = query.filter(University.region.ilike(f"%{region}%"))

        if is_public is not None:
            query = query.filter(University.is_public == is_public)

        if is_active is not None:
            query = query.filter(University.is_active == is_active)

        total = query.count()
        universities = query.order_by(University.name).offset((page - 1) * size).limit(size).all()

        return {
            "universities": universities,
            "total": total,
            "page": page,
            "size": size,
        }

    def update(self, university_id: str, university_data: UniversityUpdate) -> University:
        university = self.get_by_id(university_id)

        update_data = university_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(university, field, value)

        self.db.commit()
        self.db.refresh(university)
        return university

    def delete(self, university_id: str) -> bool:
        university = self.get_by_id(university_id)
        self.db.delete(university)
        self.db.commit()
        return True

    def get_regions(self) -> List[str]:
        regions = self.db.query(University.region).filter(University.region.isnot(None)).distinct().all()
        return [r[0] for r in regions if r[0]]