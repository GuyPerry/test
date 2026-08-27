"""Unit tests for the answer_question tool."""
import pytest
from app.tools import answer_question


def test_answer_question_returns_response():
    result = answer_question.invoke({"question": "What is the agenda for today?"})
    assert isinstance(result, str)
    assert len(result) > 0


def test_answer_question_includes_original_question():
    question = "How long is each session?"
    result = answer_question.invoke({"question": question})
    assert question in result or "question" in result.lower()
