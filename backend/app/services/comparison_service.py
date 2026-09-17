from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.core.exceptions import NotFoundException, ConflictException
from app.models.admission import Admission
from app.schemas.comparison import AdmissionCreate, AdmissionUpdate


class AdmissionService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, admission_data: AdmissionCreate) -> Admission:
        admission = Admission(**admission_data.model_dump())
        self.db.add(admission)
        self.db.commit()
        self.db.refresh(admission)
        return admission

    def get_by_id(self, admission_id: str) -> Admission:
        admission = self.db.query(Admission).filter(Admission.id == admission_id).first()
        if not admission:
            raise NotFoundException("Admission", admission_id)
        return admission

    def get_all(
        self,
        page: int = 1,
        size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        university_id: Optional[str] = None,
        programme_id: Optional[str] = None,
        academic_year: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Dict[str, Any]:
        query = self.db.query(Admission)

        if search:
            query = query.filter(
                or_(
                    Admission.intake.ilike(f"%{search}%"),
                    Admission.requirements.ilike(f"%{search}%"),
                )
            )

        if status:
            query = query.filter(Admission.status == status)

        if university_id:
            query = query.filter(Admission.university_id == university_id)

        if programme_id:
            query = query.filter(Admission.programme_id == programme_id)

        if academic_year:
            query = query.filter(Admission.academic_year == academic_year)

        if is_active is not None:
            query = query.filter(Admission.is_active == is_active)

        total = query.count()
        admissions = query.order_by(Admission.application_deadline).offset((page - 1) * size).limit(size).all()

        return {
            "admissions": admissions,
            "total": total,
            "page": page,
            "size": size,
        }

    def update(self, admission_id: str, admission_data: AdmissionUpdate) -> Admission:
        admission = self.get_by_id(admission_id)

        update_data = admission_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(admission, field, value)

        self.db.commit()
        self.db.refresh(admission)
        return admission

    def delete(self, admission_id: str) -> bool:
        admission = self.get_by_id(admission_id)
        self.db.delete(admission)
        self.db.commit()
        return True

    def get_open_admissions(self, limit: int = 10) -> List[Admission]:
        return (
            self.db.query(Admission)
            .filter(Admission.status == "open", Admission.is_active == True)
            .order_by(Admission.application_deadline)
            .limit(limit)
            .all()
        )