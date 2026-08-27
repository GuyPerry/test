"""Unit tests for the complete_session tool."""
import pytest
from app.tools import complete_session


def test_complete_session_with_feedback():
    result = complete_session.invoke({"feedback": "It was very informative!"})
    assert "feedback" in result.lower() or "thank" in result.lower()
    assert "It was very informative!" in result


def test_complete_session_without_feedback():
    result = complete_session.invoke({"feedback": ""})
    assert "thank" in result.lower() or "workshop" in result.lower()
