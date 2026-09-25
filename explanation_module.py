from ai_service import GeminiService, service


def explain_concept(topic: str, ai: GeminiService = service) -> tuple[str, str]:
    if ai.enabled:
        prompt = (
            "Explain this educational concept for a curious beginner. Use plain language, "
            "a short analogy, and 3 concise key points. Avoid unsupported claims.\n\n"
            f"Concept: {topic}"
        )
        try:
            return ai.generate(prompt), "gemini"
        except RuntimeError:
            pass

    return (
        f"{topic} is an idea or process that can be understood by identifying what it is, "
        "how it works, and why it matters. Start with a simple definition, connect it to "
        "a familiar example, then test your understanding with a small example of your own.",
        "offline",
    )
