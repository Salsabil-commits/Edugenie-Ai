from __future__ import annotations

import time
from typing import Any

from config import get_settings


class GeminiService:
    """Small adapter around Gemini so features can be tested without a network call."""

    def __init__(self) -> None:
        settings = get_settings()
        self.model_name = settings.gemini_model
        self._client: Any = None
        if settings.gemini_api_key:
            from google import genai

            self._client = genai.Client(api_key=settings.gemini_api_key)

    @property
    def enabled(self) -> bool:
        return self._client is not None

    def generate(self, prompt: str, *, response_mime_type: str | None = None) -> str:
        if not self._client:
            raise RuntimeError("Gemini is not configured. Add GEMINI_API_KEY to .env.")
        config: dict[str, str] = {}
        if response_mime_type:
            config["response_mime_type"] = response_mime_type
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config or None,
                )
                break
            except Exception as error:
                last_error = error
                message = str(error)
                transient = any(code in message for code in ("429", "500", "502", "503", "504"))
                if not transient or attempt == 2:
                    raise RuntimeError(f"Gemini request failed: {error}") from error
                time.sleep(2**attempt)
        else:
            raise RuntimeError(f"Gemini request failed: {last_error}") from last_error
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()


service = GeminiService()
