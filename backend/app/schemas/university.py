from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class UniversityBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    short_name: str = Field(..., min_length=2, max_length=50)
    tcu_code: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=100)
    logo_url: Optional[HttpUrl] = None
    is_public: bool = True
    established_year: Optional[int] = None
    accreditation_status: Optional[str] = Field(None, max_length=50)


class UniversityCreate(UniversityBase):
    pass


class UniversityUpdate(UniversityBase):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    short_name: Optional[str] = Field(None, min_length=2, max_length=50)
    is_active: Optional[bool] = None


class UniversityResponse(UniversityBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UniversityListResponse(BaseModel):
    universities: List[UniversityResponse]
    total: int
    page: int
    size: int