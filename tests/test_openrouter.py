"""Focused tests for query_model failure handling."""

import asyncio

from backend import council, openrouter


class _RaisingAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    async def post(self, *args, **kwargs):
        raise ConnectionError("connection refused")


def test_query_model_returns_error_detail_on_failure(monkeypatch) -> None:
    """A failed request must surface the real error, not silently become None."""
    monkeypatch.setattr(openrouter.httpx, "AsyncClient", _RaisingAsyncClient)

    result = asyncio.run(
        openrouter.query_model("some-model", [{"role": "user", "content": "hi"}])
    )

    assert result == {"content": None, "error": "connection refused"}


def test_query_model_failure_does_not_write_to_stdout(monkeypatch, capsys) -> None:
    """stdout is the MCP stdio JSON-RPC wire; failures must never write there."""
    monkeypatch.setattr(openrouter.httpx, "AsyncClient", _RaisingAsyncClient)

    asyncio.run(
        openrouter.query_model("some-model", [{"role": "user", "content": "hi"}])
    )

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "connection refused" in captured.err


def test_stage3_surfaces_real_error_on_chairman_failure(monkeypatch) -> None:
    """The chairman-failure fallback must include the actual error, not a generic string."""

    async def fake_query_model(model, messages, timeout=120.0):
        return {"content": None, "error": "rate limited"}

    monkeypatch.setattr(council, "query_model", fake_query_model)

    result = asyncio.run(council.stage3_synthesize_final("question", [], []))

    assert "rate limited" in result["response"]
