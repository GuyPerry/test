"""Unit tests for the greet_participant tool."""
import pytest
from app.tools import greet_participant


def test_greet_with_name_and_role():
    result = greet_participant.invoke({"name": "Alice", "role": "Developer"})
    assert "Alice" in result
    assert "Developer" in result


def test_greet_with_name_only():
    result = greet_participant.invoke({"name": "Bob", "role": ""})
    assert "Bob" in result
    assert "workshop assistant" in result.lower() or "welcome" in result.lower()


def test_greet_with_role_only():
    result = greet_participant.invoke({"name": "", "role": "Manager"})
    assert "Manager" in result


def test_greet_no_info():
    result = greet_participant.invoke({"name": "", "role": ""})
    assert "welcome" in result.lower()
