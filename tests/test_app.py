from fastapi.testclient import TestClient

from main import app
from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz


client = TestClient(app)


class BrokenGemini:
    enabled = True

    def generate(self, *args, **kwargs):
        raise RuntimeError("Gemini request failed: 404 NOT_FOUND")


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_page_loads() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Turn questions into" in response.text


def test_all_feature_routes_work_without_api_key() -> None:
    cases = [
        ("/qa", {"question": "What is the largest ocean?"}),
        ("/explain", {"text": "photosynthesis"}),
        ("/summarize", {"text": "Learning is strengthened by practice and retrieval."}),
        ("/quiz", {"text": "The water cycle includes evaporation and precipitation."}),
        ("/learn/recommendations", {"topic": "SQL", "level": "beginner", "weekly_hours": 5}),
    ]
    for route, payload in cases:
        response = client.post(route, json=payload)
        assert response.status_code == 200, response.text
        assert response.json()["source"] == "offline"


def test_validation_rejects_empty_question() -> None:
    response = client.post("/qa", json={"question": ""})
    assert response.status_code == 422


def test_gemini_failure_uses_local_fallback() -> None:
    ai = BrokenGemini()
    explanation, explanation_source = explain_concept("gravity", ai)
    answer, answer_source = answer_question("What is gravity?", ai)
    quiz, quiz_source = generate_quiz("Gravity attracts objects toward one another.", ai)

    assert explanation_source == "offline"
    assert answer_source == "offline"
    assert quiz_source == "offline"
    assert explanation
    assert answer
    assert len(quiz) == 3


def test_offline_summary_reports_missing_gemini() -> None:
    passage = " ".join(f"word-{index}" for index in range(100))
    response = client.post("/summarize", json={"text": passage})

    assert response.status_code == 200
    assert response.json()["source"] == "offline"
    assert response.json()["result"] == (
        "Gemini is not configured. Add GEMINI_API_KEY to .env to generate an AI summary."
    )
