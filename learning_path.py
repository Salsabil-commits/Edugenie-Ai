from ai_service import GeminiService, service


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weekly_hours: int = 5,
    ai: GeminiService = service,
) -> tuple[str, str]:
    if ai.enabled:
        prompt = (
            "Create a practical learning path in Markdown for the requested topic. Include "
            "a brief goal, four stages from foundations to projects, an estimated timeline "
            "based on the weekly hours, practice ideas, and reliable resource types. "
            "Tailor the starting point to the learner's level.\n\n"
            f"Topic: {topic}\nLevel: {level}\nHours per week: {weekly_hours}"
        )
        try:
            return ai.generate(prompt), "gemini"
        except RuntimeError:
            pass

    return (
        f"## {topic.title()} learning path\n\n"
        f"**Starting level:** {level}  \n**Pace:** {weekly_hours} hours/week\n\n"
        "### Stage 1: Foundations\nLearn the vocabulary, core ideas, and basic examples.\n\n"
        "### Stage 2: Guided practice\nWork through small exercises and explain each solution.\n\n"
        "### Stage 3: Applied skills\nBuild a small project using the concepts.\n\n"
        "### Stage 4: Next steps\nReview gaps, read primary documentation, and attempt a larger project.\n\n"
        "**Weekly rhythm:** 40% learning, 40% practice, 20% review.",
        "offline",
    )
