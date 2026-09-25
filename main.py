from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import LearningPathRequest, QuestionRequest, QuizResponse, TextRequest, TextResponse
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie API", version="1.0.0", description="A Gemini-powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/qa", response_model=TextResponse)
async def qa(payload: QuestionRequest) -> TextResponse:
    result, source = answer_question(payload.question)
    return TextResponse(result=result, source=source)


@app.post("/explain", response_model=TextResponse)
async def explain(payload: TextRequest) -> TextResponse:
    result, source = explain_concept(payload.text)
    return TextResponse(result=result, source=source)


@app.post("/summarize", response_model=TextResponse)
async def summarize(payload: TextRequest) -> TextResponse:
    try:
        result, source = summarize_text(payload.text)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return TextResponse(result=result, source=source)


@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: TextRequest) -> QuizResponse:
    questions, source = generate_quiz(payload.text)
    return QuizResponse(questions=questions, source=source)


@app.post("/learn/recommendations", response_model=TextResponse)
async def recommendations(payload: LearningPathRequest) -> TextResponse:
    result, source = get_learning_recommendations(payload.topic, payload.level, payload.weekly_hours)
    return TextResponse(result=result, source=source)
