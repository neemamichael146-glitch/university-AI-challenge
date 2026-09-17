from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    filters: Optional[Dict[str, Any]] = None
    limit: int = Field(default=10, ge=1, le=50)
    offset: int = Field(default=0, ge=0)


class SearchResult(BaseModel):
    id: str
    type: str
    title: str
    snippet: str
    url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    relevance_score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    query: str
    took_ms: int