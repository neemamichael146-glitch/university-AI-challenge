from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.core.exceptions import NotFoundException, ConflictException
from app.models.scholarship import Scholarship
from app.schemas.eligibility import ScholarshipCreate, ScholarshipUpdate


class ScholarshipService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, scholarship_data: ScholarshipCreate) -> Scholarship:
        scholarship = Scholarship(**scholarship_data.model_dump())
        self.db.add(scholarship)
        self.db.commit()
        self.db.refresh(scholarship)
        return scholarship

    def get_by_id(self, scholarship_id: str) -> Scholarship:
        scholarship = self.db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
        if not scholarship:
            raise NotFoundException("Scholarship", scholarship_id)
        return scholarship

    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        search: Optional[str] = None,
        type: Optional[str] = None,
        university_id: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_featured: Optional[bool] = None,
    ) -> Dict[str, Any]:
        query = self.db.query(Scholarship)

        if search:
            query = query.filter(
                or_(
                    Scholarship.name.ilike(f"%{search}%"),
                    Scholarship.description.ilike(f"%{search}%"),
                )
            )

        if type:
            query = query.filter(Scholarship.type == type)

        if university_id:
            query = query.filter(Scholarship.university_id == university_id)

        if is_active is not None:
            query = query.filter(Scholarship.is_active == is_active)

        if is_featured is not None:
            query = query.filter(Scholarship.is_featured == is_featured)

        total = query.count()
        scholarships = query.order_by(Scholarship.application_deadline).offset((page - 1) * size).limit(size).all()

        return {
            "scholarships": scholarships,
            "total": total,
            "page": page,
            "size": size,
        }

    def update(self, scholarship_id: str, scholarship_data: ScholarshipUpdate) -> Scholarship:
        scholarship = self.get_by_id(scholarship_id)

        update_data = scholarship_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(scholarship, field, value)

        self.db.commit()
        self.db.refresh(scholarship)
        return scholarship

    def delete(self, scholarship_id: str) -> bool:
        scholarship = self.get_by_id(scholarship_id)
        self.db.delete(scholarship)
        self.db.commit()
        return True

    def get_types(self) -> List[str]:
        return ["full", "partial", "tuition_waiver", "stipend", "research_grant"]