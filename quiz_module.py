from __future__ import annotations

import json
import re

from ai_service import GeminiService, service
from schemas import QuizQuestion


def _parse_json(text: str) -> list[dict]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    payload = json.loads(cleaned)
    if isinstance(payload, dict):
        payload = payload.get("questions", [])
    if not isinstance(payload, list):
        raise ValueError("Quiz response must be a list.")
    return payload


def generate_quiz(text: str, ai: GeminiService = service) -> tuple[list[QuizQuestion], str]:
    if ai.enabled:
        prompt = (
            "Generate exactly 3 multiple-choice questions from this passage. Return only valid "
            "JSON with a questions array. Each item must have question, options (exactly four "
            "strings), answer (one option string), and explanation.\n\nPassage:\n" + text
        )
        try:
            questions = [
                QuizQuestion.model_validate(item)
                for item in _parse_json(ai.generate(prompt, response_mime_type="application/json"))
            ]
            return questions[:3], "gemini"
        except (RuntimeError, ValueError, TypeError, KeyError):
            pass

    return [
        QuizQuestion(
            question="What is the best first step when studying this material?",
            options=["Identify the core idea", "Skip the examples", "Memorize every word", "Avoid questions"],
            answer="Identify the core idea",
            explanation="Understanding the central idea creates a useful framework for details.",
        ),
        QuizQuestion(
            question="Which approach supports durable learning?",
            options=["Active practice", "Passive rereading only", "No review", "Guessing"],
            answer="Active practice",
            explanation="Retrieval and application reveal what you understand.",
        ),
        QuizQuestion(
            question="How should a learner handle a difficult concept?",
            options=["Break it into smaller parts", "Ignore it", "Add unrelated facts", "Stop reviewing"],
            answer="Break it into smaller parts",
            explanation="Smaller steps make complex material easier to reason about.",
        ),
    ], "offline"
