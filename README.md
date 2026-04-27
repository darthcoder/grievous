# grievous

> *"Your lightsabers will make a fine addition to my collection."*

A hallucination engine. Typed pseudorandom data via Anthropic API. MCP server.

---

## ⚠️ No Guarantees

This is **not** a PRNG. This is **not** a test data framework with schema validation. This is a footgun with good trigger discipline expected of the operator.

- Output is **plausible**, not **correct**
- Output is **nondeterministic** — same schema, different result every time
- Output is **not validated** — if the model returns garbage, you get garbage
- Output is **not uniform** — LLMs have opinions about what "random" looks like

**Good for:** seeding dev DBs, one-off REPL sessions, agentic pipelines that need typed data fast, anywhere plausible beats uniform.

**Not for:** cryptography, reproducibility, performance-sensitive paths, production data.

---

## Install

```bash
uv sync
```

## Configure

```bash
cp .env.example .env
# add your ANTHROPIC_API_KEY
```

## Run as MCP server

```bash
uv run grievous
```

Add to your MCP client config (e.g. Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "grievous": {
      "command": "uv",
      "args": ["run", "grievous"],
      "cwd": "/path/to/grievous",
      "env": {
        "ANTHROPIC_API_KEY": "your-key-here"
      }
    }
  }
}
```

---

## Tool

### `generate`

```
generate(schema, count=1, model="claude-haiku-4-5-20251001")
```

**`schema`** — freeform string. Natural language or JSON schema, both work:

```
"a User with name, age, email"
"a 4x4 float32 tensor"
'{"type": "object", "properties": {"sku": {"type": "string"}, "price": {"type": "number"}}}'
"an ISO 8601 timestamp from sometime in 2019"
"a plausible Indian phone number"
```

**`count`** — how many. Default 1.

**`model`** — Anthropic model to use. Haiku by default for speed and cost.

**Returns** — parsed JSON if the model cooperated. Raw string if it didn't. Both are valid outcomes.

---

## Roadmap

- **v1.0** — Anthropic API backend (current)
- **v2.0** — Ollama/local model support (if there's interest)

---

## Why "Grievous"

He's a General (general-purpose). He collects everything you hand him (schemas, types, whatever). He's chaotic but capable. He doesn't work for one army.

The cough is the nondeterminism.
