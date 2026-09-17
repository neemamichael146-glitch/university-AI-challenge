from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class ScholarshipBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    type: str = Field(..., pattern="^(full|partial|tuition_waiver|stipend|research_grant)$")
    amount_tzs: Optional[float] = Field(None, ge=0)
    amount_usd: Optional[float] = Field(None, ge=0)
    coverage_details: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    application_requirements: Optional[str] = None
    application_deadline: datetime
    application_url: Optional[str] = None
    contact_email: Optional[str] = Field(None, max_length=255)
    number_of_awards: Optional[int] = Field(None, ge=1)
    is_featured: bool = False


class ScholarshipCreate(ScholarshipBase):
    university_id: str


class ScholarshipUpdate(ScholarshipBase):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    type: Optional[str] = Field(None, pattern="^(full|partial|tuition_waiver|stipend|research_grant)$")
    is_active: Optional[bool] = None


class ScholarshipResponse(ScholarshipBase):
    id: str
    university_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScholarshipListResponse(BaseModel):
    scholarships: List[ScholarshipResponse]
    total: int
    page: int
    size: int


class EligibilityCheckRequest(BaseModel):
    programme_id: str
    qualifications: List[Dict[str, Any]]
    subjects: Optional[List[str]] = None
    grades: Optional[Dict[str, str]] = None


class EligibilityResult(BaseModel):
    is_eligible: bool
    score: float = Field(..., ge=0, le=100)
    requirements_met: List[str]
    requirements_missing: List[str]
    recommendations: List[str]
    programme_requirements: Dict[str, Any]


class EligibilityComparison(BaseModel):
    programme_id: str
    programme_name: str
    is_eligible: bool
    score: float
    missing_requirements: List[str]