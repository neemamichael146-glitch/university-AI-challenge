from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AdmissionBase(BaseModel):
    academic_year: str = Field(..., min_length=4, max_length=20)
    intake: str = Field(..., min_length=2, max_length=50)
    status: str = Field(default="upcoming", pattern="^(open|closed|upcoming|extended)$")
    application_start: datetime
    application_deadline: datetime
    extended_deadline: Optional[datetime] = None
    requirements: Optional[str] = None
    application_url: Optional[str] = None
    contact_email: Optional[str] = Field(None, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class AdmissionCreate(AdmissionBase):
    university_id: str
    programme_id: Optional[str] = None


class AdmissionUpdate(AdmissionBase):
    academic_year: Optional[str] = Field(None, min_length=4, max_length=20)
    intake: Optional[str] = Field(None, min_length=2, max_length=50)
    status: Optional[str] = Field(None, pattern="^(open|closed|upcoming|extended)$")
    is_active: Optional[bool] = None


class AdmissionResponse(AdmissionBase):
    id: str
    university_id: str
    programme_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AdmissionListResponse(BaseModel):
    admissions: List[AdmissionResponse]
    total: int
    page: int
    size: int