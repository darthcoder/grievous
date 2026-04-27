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
pip install grievous-mcp
```

Set your API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Typical Usage

### From Python

```python
from grievous.backend import generate

# Single object — natural language schema
user = generate("a User with name, age, email, and city")
# {"name": "Priya Nair", "age": 34, "email": "priya.nair@example.com", "city": "Bangalore"}

# Batch
products = generate("a Product with id, name, price_usd, and category", count=5)
# [{"id": 1, "name": "Wireless Headphones", ...}, ...]

# JSON Schema works too
import json
schema = json.dumps({
    "type": "object",
    "properties": {
        "transaction_id": {"type": "string", "format": "uuid"},
        "amount_usd":     {"type": "number"},
        "status":         {"type": "string", "enum": ["pending", "cleared", "failed"]},
    }
})
txn = generate(schema)
# {"transaction_id": "a3f1...", "amount_usd": 142.5, "status": "cleared"}

# Freeform — anything the model can hallucinate
tensor = generate("a 4x4 float32 matrix, values between -1 and 1")
timestamp = generate("an ISO 8601 timestamp from sometime in 2019")
phone = generate("a plausible Indian mobile number")
```

Returns parsed JSON if the model cooperated. Raw string if it didn't. No exceptions.

---

## As an MCP Server

Run directly:

```bash
grievous
```

Add to your MCP client config (e.g. Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "grievous": {
      "command": "grievous",
      "env": {
        "ANTHROPIC_API_KEY": "your-key-here"
      }
    }
  }
}
```

### Tool: `generate`

```
generate(schema, count=1, model="claude-haiku-4-5-20251001")
```

| Arg | Type | Default | Description |
|-----|------|---------|-------------|
| `schema` | string | — | Natural language or JSON Schema |
| `count` | int | 1 | Number of instances |
| `model` | string | `claude-haiku-4-5-20251001` | Any Anthropic model |

---

## Roadmap

- **v1.0** — Anthropic API backend (current)
- **v2.0** — Ollama/local model support (if there's interest)

---

## Why "Grievous"

He's a General (general-purpose). He collects everything you hand him (schemas, types, whatever). He's chaotic but capable. He doesn't work for one army.

The cough is the nondeterminism.
