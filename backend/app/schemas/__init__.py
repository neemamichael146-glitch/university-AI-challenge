from app.schemas.auth import UserCreate, UserLogin, UserResponse, TokenResponse, RefreshTokenRequest
from app.schemas.university import UniversityCreate, UniversityUpdate, UniversityResponse, UniversityListResponse
from app.schemas.programmes import ProgrammeCreate, ProgrammeUpdate, ProgrammeResponse, ProgrammeListResponse, ProgrammeComparison
from app.schemas.comparison import AdmissionCreate, AdmissionUpdate, AdmissionResponse, AdmissionListResponse
from app.schemas.eligibility import ScholarshipCreate, ScholarshipUpdate, ScholarshipResponse, ScholarshipListResponse
from app.schemas.eligibility import EligibilityCheckRequest, EligibilityResult, EligibilityComparison
from app.schemas.chat import ChatRequest, ChatResponse, ConversationCreate, ConversationUpdate, ConversationResponse, MessageResponse, ConversationWithMessages
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.schemas.admin import DashboardStats, UserAdminResponse, UserListResponse, SystemHealth

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "TokenResponse", "RefreshTokenRequest",
    "UniversityCreate", "UniversityUpdate", "UniversityResponse", "UniversityListResponse",
    "ProgrammeCreate", "ProgrammeUpdate", "ProgrammeResponse", "ProgrammeListResponse", "ProgrammeComparison",
    "AdmissionCreate", "AdmissionUpdate", "AdmissionResponse", "AdmissionListResponse",
    "ScholarshipCreate", "ScholarshipUpdate", "ScholarshipResponse", "ScholarshipListResponse",
    "EligibilityCheckRequest", "EligibilityResult", "EligibilityComparison",
    "ChatRequest", "ChatResponse", "ConversationCreate", "ConversationUpdate", "ConversationResponse", "MessageResponse", "ConversationWithMessages",
    "SearchRequest", "SearchResponse", "SearchResult",
    "DashboardStats", "UserAdminResponse", "UserListResponse", "SystemHealth",
]