from ai_service import GeminiService, service


def answer_question(question: str, ai: GeminiService = service) -> tuple[str, str]:
    if ai.enabled:
        prompt = (
            "Answer the student's question accurately and concisely. State uncertainty when "
            "appropriate and explain essential reasoning in accessible language.\n\n"
            f"Question: {question}"
        )
        try:
            return ai.generate(prompt), "gemini"
        except RuntimeError:
            pass

    return (
        "Gemini is not configured yet, so I cannot look up that answer. Add GEMINI_API_KEY "
        "to your .env file, restart the server, and ask the question again.",
        "offline",
    )
