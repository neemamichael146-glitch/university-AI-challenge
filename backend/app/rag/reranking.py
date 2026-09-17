from typing import List, Dict, Any, Optional
from app.ai.router import AIModelRouter


class RerankingService:
    def __init__(self):
        self.router = AIModelRouter()

    async def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 5,
        provider: str = None,
    ) -> List[Dict[str, Any]]:
        if not documents:
            return []
        
        if len(documents) <= top_k:
            return documents
        
        prompt = self._build_rerank_prompt(query, documents)
        
        try:
            response = await self.router.generate_response(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500,
                provider=provider,
            )
            
            ranked_indices = self._parse_rerank_response(response["message"], len(documents))
            reranked = [documents[i] for i in ranked_indices if i < len(documents)]
            return reranked[:top_k]
        except Exception:
            return documents[:top_k]

    def _build_rerank_prompt(self, query: str, documents: List[Dict[str, Any]]) -> str:
        doc_list = "\n\n".join([
            f"[{i}] {doc.get('content', '')[:500]}..."
            for i, doc in enumerate(documents)
        ])
        
        return f"""Given the query: "{query}"

Rank the following documents by relevance (most relevant first). Return only the indices in order, comma-separated.

Documents:
{doc_list}

Return format: 2,0,4,1,3"""

    def _parse_rerank_response(self, response: str, num_docs: int) -> List[int]:
        try:
            indices = [int(x.strip()) for x in response.split(',')]
            valid_indices = [i for i in indices if 0 <= i < num_docs]
            seen = set()
            unique = []
            for i in valid_indices:
                if i not in seen:
                    seen.add(i)
                    unique.append(i)
            for i in range(num_docs):
                if i not in seen:
                    unique.append(i)
            return unique
        except Exception:
            return list(range(num_docs))