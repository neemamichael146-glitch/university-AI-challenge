from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.core.exceptions import NotFoundException, ConflictException
from app.models.programme import Programme
from app.schemas.programmes import ProgrammeCreate, ProgrammeUpdate


class ProgrammeService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, programme_data: ProgrammeCreate) -> Programme:
        existing = self.db.query(Programme).filter(Programme.code == programme_data.code).first()
        if existing:
            raise ConflictException("Programme with this code already exists")

        programme = Programme(**programme_data.model_dump())
        self.db.add(programme)
        self.db.commit()
        self.db.refresh(programme)
        return programme

    def get_by_id(self, programme_id: str) -> Programme:
        programme = self.db.query(Programme).filter(Programme.id == programme_id).first()
        if not programme:
            raise NotFoundException("Programme", programme_id)
        return programme

    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        search: Optional[str] = None,
        level: Optional[str] = None,
        university_id: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_featured: Optional[bool] = None,
    ) -> Dict[str, Any]:
        query = self.db.query(Programme)

        if search:
            query = query.filter(
                or_(
                    Programme.name.ilike(f"%{search}%"),
                    Programme.code.ilike(f"%{search}%"),
                )
            )

        if level:
            query = query.filter(Programme.level == level)

        if university_id:
            query = query.filter(Programme.university_id == university_id)

        if is_active is not None:
            query = query.filter(Programme.is_active == is_active)

        if is_featured is not None:
            query = query.filter(Programme.is_featured == is_featured)

        total = query.count()
        programmes = query.order_by(Programme.name).offset((page - 1) * size).limit(size).all()

        return {
            "programmes": programmes,
            "total": total,
            "page": page,
            "size": size,
        }

    def update(self, programme_id: str, programme_data: ProgrammeUpdate) -> Programme:
        programme = self.get_by_id(programme_id)

        update_data = programme_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(programme, field, value)

        self.db.commit()
        self.db.refresh(programme)
        return programme

    def delete(self, programme_id: str) -> bool:
        programme = self.get_by_id(programme_id)
        self.db.delete(programme)
        self.db.commit()
        return True

    def get_levels(self) -> List[str]:
        return ["certificate", "diploma", "bachelor", "master", "phd"]