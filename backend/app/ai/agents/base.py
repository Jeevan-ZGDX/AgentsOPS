import json
import logging
from typing import Optional, Any
from openai import OpenAI
from app.core.config import get_settings
from app.ai.memory.shared_memory import SharedMemory

logger = logging.getLogger(__name__)
settings = get_settings()


class BaseAgent:
    def __init__(self, model: Optional[str] = None):
        self.model = model or settings.OPENAI_MODEL
        self.client = self._create_client()

    def _create_client(self) -> OpenAI:
        if settings.NVIDIA_NIM_API_KEY:
            return OpenAI(
                api_key=settings.NVIDIA_NIM_API_KEY,
                base_url=settings.NVIDIA_NIM_BASE_URL,
            )
        return OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
        )

    def _call_llm(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content or "{}"
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return "{}"

    def _parse_json(self, text: str) -> dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            try:
                start = text.index("{")
                end = text.rindex("}") + 1
                return json.loads(text[start:end])
            except (ValueError, json.JSONDecodeError):
                logger.warning("Failed to parse LLM response as JSON")
                return {}
