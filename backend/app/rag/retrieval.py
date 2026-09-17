from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.document import Document


class RetrievalService:
    def __init__(self, db: Session):
        self.db = db

    def search_by_vector(
        self,
        query_embedding: List[float],
        limit: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        try:
            embedding_str = '[' + ','.join(str(x) for x in query_embedding) + ']'
            
            query = """
                SELECT id, content, metadata, 1 - (embedding <=> :embedding) as similarity
                FROM documents
                WHERE is_processed = true AND embedding IS NOT NULL
            """
            
            if filter_dict:
                for key, value in filter_dict.items():
                    query += f" AND metadata->>'{key}' = '{value}'"
            
            query += " ORDER BY similarity DESC LIMIT :limit"
            
            result = self.db.execute(text(query), {"embedding": embedding_str, "limit": limit})
            
            return [
                {
                    "id": row.id,
                    "content": row.content,
                    "metadata": row.metadata,
                    "similarity": float(row.similarity),
                }
                for row in result
            ]
        except Exception as e:
            return []

    def search_by_keyword(
        self,
        query: str,
        limit: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        try:
            search_query = """
                SELECT id, content, metadata,
                       ts_rank_cd(to_tsvector('english', content), plainto_tsquery('english', :query)) as rank
                FROM documents
                WHERE is_processed = true
                  AND to_tsvector('english', content) @@ plainto_tsquery('english', :query)
            """
            
            if filter_dict:
                for key, value in filter_dict.items():
                    search_query += f" AND metadata->>'{key}' = '{value}'"
            
            search_query += " ORDER BY rank DESC LIMIT :limit"
            
            result = self.db.execute(text(search_query), {"query": query, "limit": limit})
            
            return [
                {
                    "id": row.id,
                    "content": row.content,
                    "metadata": row.metadata,
                    "similarity": float(row.rank),
                }
                for row in result
            ]
        except Exception as e:
            return []

    def hybrid_search(
        self,
        query: str,
        query_embedding: List[float],
        limit: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> List[Dict[str, Any]]:
        vector_results = self.search_by_vector(query_embedding, limit * 2, filter_dict)
        keyword_results = self.search_by_keyword(query, limit * 2, filter_dict)
        
        combined = {}
        for r in vector_results:
            combined[r["id"]] = {**r, "vector_score": r["similarity"], "keyword_score": 0.0}
        
        for r in keyword_results:
            if r["id"] in combined:
                combined[r["id"]]["keyword_score"] = r["similarity"]
            else:
                combined[r["id"]] = {**r, "vector_score": 0.0, "keyword_score": r["similarity"]}
        
        for doc in combined.values():
            doc["similarity"] = (
                doc["vector_score"] * vector_weight + doc["keyword_score"] * keyword_weight
            )
        
        sorted_results = sorted(combined.values(), key=lambda x: x["similarity"], reverse=True)
        return sorted_results[:limit]