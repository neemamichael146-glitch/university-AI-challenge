from typing import List, Dict, Any, Optional
import openai
from app.ai.provider import AIProvider
from app.core.config import settings


class OpenAIProvider(AIProvider):
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._model = settings.LLM_MODEL

    @property
    def name(self) -> str:
        return "openai"

    @property
    def model(self) -> str:
        return self._model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        try:
            system_prompt = self._build_system_prompt(context)
            all_messages = [{"role": "system", "content": system_prompt}] + messages

            response = await self.client.chat.completions.create(
                model=self._model,
                messages=all_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return {
                "message": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens if response.usage else None,
                "model": self._model,
                "sources": [],
            }
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            response = await self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=texts,
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            raise Exception(f"OpenAI embeddings error: {str(e)}")

    def _build_system_prompt(self, context: Optional[Dict[str, Any]]) -> str:
        base_prompt = """You are ChuoAI, an AI assistant for Tanzanian university admissions.
You help students with:
- University and programme information
- Admission requirements and deadlines
- Scholarship opportunities
- TCU (Tanzania Commission for Universities) guidelines
- Course comparisons and eligibility checks

Provide accurate, helpful, and concise responses. Always cite sources when available.
If you don't know something, say so rather than guessing."""
        
        if context:
            if context.get("programmes"):
                base_prompt += f"\n\nRelevant programmes: {context['programmes']}"
            if context.get("universities"):
                base_prompt += f"\nRelevant universities: {context['universities']}"
            if context.get("admissions"):
                base_prompt += f"\nRelevant admissions: {context['admissions']}"
        
        return base_prompt