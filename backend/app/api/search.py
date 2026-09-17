from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.search import SearchRequest, SearchResponse, SearchResult

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("", response_model=SearchResponse)
async def search(
    search_request: SearchRequest,
    db: Session = Depends(get_db),
):
    results = [
        SearchResult(
            id="1",
            type="programme",
            title="Computer Science",
            snippet="Bachelor of Science in Computer Science...",
            relevance_score=0.95,
        ),
        SearchResult(
            id="2",
            type="university",
            title="University of Dar es Salaam",
            snippet="Leading public university in Tanzania...",
            relevance_score=0.88,
        ),
    ]
    
    return SearchResponse(
        results=results,
        total=len(results),
        query=search_request.query,
        took_ms=15,
    )


@router.get("/suggestions")
async def get_suggestions(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=20)):
    suggestions = [
        "Computer Science",
        "Business Administration",
        "Medicine",
        "Engineering",
        "Law",
        "Education",
    ]
    filtered = [s for s in suggestions if q.lower() in s.lower()]
    return {"suggestions": filtered[:limit]}