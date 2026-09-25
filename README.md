# Edugenie-Ai

EduGenie is a lightweight FastAPI learning assistant with a responsive browser interface. It supports question answering, concept explanations, passage summaries, three-question MCQ quizzes, and personalized learning paths. Gemini powers the generation when an API key is present; an offline preview mode keeps the app runnable without credentials.

## VS Code setup

1. Open the `/home/salsabil/EduGenie` folder in VS Code.
2. Confirm Python 3.10 or newer is available:

   ```bash
   python3 --version
   ```

3. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and set `GEMINI_API_KEY` from Google AI Studio. Leave it blank to use offline preview mode. You can change `GEMINI_MODEL` if your account uses another supported Gemini model.

## Run

With the virtual environment active:

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000. The interactive API documentation is available at http://127.0.0.1:8000/docs.

## Test

```bash
pytest -q
```

The tests exercise the health check, page rendering, validation, and every documented API route without making external Gemini calls.

## API examples

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H 'Content-Type: application/json' \
  -d '{"question":"Why is the sky blue?"}'
```

The other routes accept the following JSON shapes:

| Route | Body |
| --- | --- |
| `/explain` | `{"text":"..."}` |
| `/summarize` | `{"text":"..."}` |
| `/quiz` | `{"text":"..."}` |
| `/learn/recommendations` | `{"topic":"SQL","level":"beginner","weekly_hours":5}` |

## Project layout

```text
main.py                 FastAPI app and routes
ai_service.py           Shared Gemini adapter
explanation_module.py   Concept explanation
qna.py                  Question answering
quiz_module.py          Structured MCQ generation
summary_module.py       Passage summarization
learning_path.py        Personalized study plans
schemas.py              Request and response validation
templates/index.html    Browser interface
static/style.css        Responsive visual styling
static/app.js           Frontend API integration
tests/test_app.py       Offline route tests
```
