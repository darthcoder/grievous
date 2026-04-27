import json
import os
import anthropic

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = (
    "You are a data hallucination engine. "
    "Return ONLY valid JSON. No preamble, no explanation, no markdown fences. "
    "Just raw JSON."
)


def build_prompt(schema: str, count: int) -> str:
    if count == 1:
        return f"Generate 1 instance of: {schema}"
    return f"Generate a JSON array of {count} instances of: {schema}"


def generate(
    schema: str,
    count: int = 1,
    model: str = DEFAULT_MODEL,
) -> object:
    """
    Hit Anthropic API, get raw response. Returns parsed JSON if possible, raw string if not.
    This is a footgun. You were warned.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": build_prompt(schema, count)},
        ],
    )

    raw = message.content[0].text.strip()

    # Best-effort fence stripping
    if raw.startswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

    # Best-effort parse — return raw string on failure, no apologies
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw
