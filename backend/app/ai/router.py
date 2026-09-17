from typing import List, Dict, Any, Optional
from app.ai.provider import AIProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.groq_provider import GroqProvider
from app.core.config import settings


class AIModelRouter:
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {}
        self._init_providers()

    def _init_providers(self):
        if settings.OPENAI_API_KEY:
            self.providers["openai"] = OpenAIProvider()
        if settings.GROQ_API_KEY:
            self.providers["groq"] = GroqProvider()

        if not self.providers:
            raise ValueError("No AI provider configured. Set OPENAI_API_KEY or GROQ_API_KEY.")

    def get_provider(self, provider_name: Optional[str] = None) -> AIProvider:
        if provider_name and provider_name in self.providers:
            return self.providers[provider_name]
        
        if settings.LLM_PROVIDER in self.providers:
            return self.providers[settings.LLM_PROVIDER]
        
        return list(self.providers.values())[0]

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        provider: Optional[str] = None,
    ) -> Dict[str, Any]:
        ai_provider = self.get_provider(provider)
        return await ai_provider.generate_response(
            messages=messages,
            context=context,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def get_embeddings(self, texts: List[str], provider: Optional[str] = None) -> List[List[float]]:
        ai_provider = self.get_provider(provider)
        return await ai_provider.get_embeddings(texts)

    def list_providers(self) -> List[str]:
        return list(self.providers.keys())