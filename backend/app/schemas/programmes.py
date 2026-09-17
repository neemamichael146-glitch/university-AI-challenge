from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProgrammeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    code: str = Field(..., min_length=2, max_length=20)
    description: Optional[str] = None
    level: str = Field(..., pattern="^(certificate|diploma|bachelor|master|phd)$")
    duration_years: int = Field(..., ge=1, le=10)
    duration_semesters: Optional[int] = Field(None, ge=1, le=20)
    credits: Optional[int] = Field(None, ge=1)
    entry_requirements: Optional[str] = None
    tuition_fee_tzs: Optional[float] = Field(None, ge=0)
    tuition_fee_usd: Optional[float] = Field(None, ge=0)
    is_featured: bool = False


class ProgrammeCreate(ProgrammeBase):
    university_id: str


class ProgrammeUpdate(ProgrammeBase):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    code: Optional[str] = Field(None, min_length=2, max_length=20)
    level: Optional[str] = Field(None, pattern="^(certificate|diploma|bachelor|master|phd)$")
    duration_years: Optional[int] = Field(None, ge=1, le=10)
    is_active: Optional[bool] = None


class ProgrammeResponse(ProgrammeBase):
    id: str
    university_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgrammeListResponse(BaseModel):
    programmes: List[ProgrammeResponse]
    total: int
    page: int
    size: int


class ProgrammeComparison(BaseModel):
    programmes: List[ProgrammeResponse]
    comparison_matrix: dict