from app.services.auth_service import AuthService
from app.services.university_service import UniversityService
from app.services.programme_service import ProgrammeService
from app.services.comparison_service import AdmissionService
from app.services.eligibility_service import ScholarshipService
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService, FAQService

__all__ = [
    "AuthService",
    "UniversityService",
    "ProgrammeService",
    "AdmissionService",
    "ScholarshipService",
    "ChatService",
    "DocumentService",
    "FAQService",
]