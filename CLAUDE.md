# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

**Grievous** is a hallucination engine — an MCP server that generates typed pseudorandom data using the Anthropic API. Given a schema (natural language or JSON Schema), it asks an LLM to "hallucinate" plausible structured data. Output is nondeterministic, unvalidated, and intentionally best-effort. Good for dev database seeding and agentic pipelines; not for production or reproducibility.

## Setup & Running

```bash
uv sync                   # install dependencies
cp .env.example .env      # add ANTHROPIC_API_KEY
uv run grievous           # start the MCP server
```

No test suite or linter is configured.

## Architecture

Two-file core under `grievous/`:

- **`server.py`** — MCP layer. Registers `generate()` as an MCP tool via `FastMCP`. Entry point called by `uv run grievous`.
- **`backend.py`** — Core logic. `generate(schema, count, model)` calls the Anthropic API, strips markdown fences from the response, and returns parsed JSON or a raw string on parse failure (no exceptions raised).

Data flow: MCP client → `server.py:generate()` → `backend.py:generate()` → Anthropic API → fence-stripped JSON parse → return.

Default model is `claude-haiku-4-5-20251001` (cost/speed optimized). The system prompt enforces JSON-only output (no preamble, no markdown).

## Key Design Decisions

- **No validation** — the tool returns raw LLM output; callers are responsible for validation.
- **Best-effort parsing** — invalid JSON returns as a raw string rather than raising an exception.
- **Haiku by default** — cheapest/fastest model is the right default for throwaway seed data.
