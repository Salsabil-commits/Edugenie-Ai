from ai_service import GeminiService, service


def summarize_text(text: str, ai: GeminiService = service) -> tuple[str, str]:
    if ai.enabled:
        prompt = (
            "Summarize the passage in 4-6 clear sentences. Preserve the central claim, "
            "important facts, and relationships. Do not add information.\n\n"
            f"Passage:\n{text}"
        )
        try:
            return ai.generate(prompt), "gemini"
        except RuntimeError as error:
            if ai.enabled:
                raise error

    return (
        "Gemini is not configured. Add GEMINI_API_KEY to .env to generate an AI summary.",
        "offline",
    )
