"""Unit tests for the provide_guidance tool."""
import pytest
from app.tools import provide_guidance


def test_provide_guidance_returns_steps():
    result = provide_guidance.invoke({"request": "What should I do next?"})
    assert isinstance(result, str)
    assert len(result) > 0


def test_provide_guidance_contains_steps():
    result = provide_guidance.invoke({"request": ""})
    # Should contain numbered steps
    assert "1." in result or "step" in result.lower() or "follow" in result.lower()
