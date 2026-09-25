from typing import Literal

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=30000)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=4000)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    weekly_hours: int = Field(default=5, ge=1, le=40)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(..., min_length=1, max_length=10)
    source: str


class TextResponse(BaseModel):
    result: str
    source: str
