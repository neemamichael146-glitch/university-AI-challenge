from typing import List, Dict, Any
from app.ai.router import AIModelRouter


class EmbeddingService:
    def __init__(self):
        self.router = AIModelRouter()

    async def get_embeddings(self, texts: List[str], provider: str = None) -> List[List[float]]:
        return await self.router.get_embeddings(texts, provider)

    async def get_embedding(self, text: str, provider: str = None) -> List[float]:
        embeddings = await self.get_embeddings([text], provider)
        return embeddings[0] if embeddings else []


async def embed_documents(documents: List[Dict[str, Any]], provider: str = None) -> List[Dict[str, Any]]:
    embedding_service = EmbeddingService()
    texts = [doc.get("content", "") for doc in documents]
    embeddings = await embedding_service.get_embeddings(texts, provider)
    
    for doc, embedding in zip(documents, embeddings):
        doc["embedding"] = embedding
    
    return documents