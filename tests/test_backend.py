import json
import pytest
from unittest.mock import MagicMock, patch

from grievous.backend import build_prompt, generate, DEFAULT_MODEL


# --- build_prompt ---

def test_build_prompt_singular():
    result = build_prompt("a User with name and email", 1)
    assert result == "Generate 1 instance of: a User with name and email"


def test_build_prompt_plural():
    result = build_prompt("a Product with SKU and price", 5)
    assert result == "Generate a JSON array of 5 instances of: a Product with SKU and price"


# --- generate: JSON parsing ---

def _mock_client(response_text: str):
    """Return a patched anthropic.Anthropic that yields response_text."""
    msg = MagicMock()
    msg.content = [MagicMock(text=response_text)]
    client = MagicMock()
    client.messages.create.return_value = msg
    return client


def test_generate_returns_parsed_json(monkeypatch):
    payload = {"name": "Alice", "age": 30}
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    with patch("grievous.backend.anthropic.Anthropic", return_value=_mock_client(json.dumps(payload))):
        result = generate("a User")
    assert result == payload


def test_generate_returns_list_for_array(monkeypatch):
    payload = [{"id": 1}, {"id": 2}]
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    with patch("grievous.backend.anthropic.Anthropic", return_value=_mock_client(json.dumps(payload))):
        result = generate("an object with id", count=2)
    assert result == payload


def test_generate_falls_back_to_raw_string_on_bad_json(monkeypatch):
    bad = "oops not json at all"
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    with patch("grievous.backend.anthropic.Anthropic", return_value=_mock_client(bad)):
        result = generate("anything")
    assert result == bad


# --- fence stripping ---

def test_generate_strips_json_fence(monkeypatch):
    payload = {"x": 42}
    fenced = f"```json\n{json.dumps(payload)}\n```"
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    with patch("grievous.backend.anthropic.Anthropic", return_value=_mock_client(fenced)):
        result = generate("anything")
    assert result == payload


def test_generate_strips_plain_fence(monkeypatch):
    payload = {"y": "hello"}
    fenced = f"```\n{json.dumps(payload)}\n```"
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    with patch("grievous.backend.anthropic.Anthropic", return_value=_mock_client(fenced)):
        result = generate("anything")
    assert result == payload


# --- model forwarding ---

def test_generate_passes_model_to_api(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    mock_client = _mock_client("{}")
    with patch("grievous.backend.anthropic.Anthropic", return_value=mock_client):
        generate("anything", model="claude-opus-4-7")
    call_kwargs = mock_client.messages.create.call_args
    assert call_kwargs.kwargs["model"] == "claude-opus-4-7"


def test_generate_uses_default_model(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    mock_client = _mock_client("{}")
    with patch("grievous.backend.anthropic.Anthropic", return_value=mock_client):
        generate("anything")
    call_kwargs = mock_client.messages.create.call_args
    assert call_kwargs.kwargs["model"] == DEFAULT_MODEL
