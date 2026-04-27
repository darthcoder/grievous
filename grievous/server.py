from mcp.server.fastmcp import FastMCP
from grievous.backend import generate as _generate, DEFAULT_MODEL

mcp = FastMCP(
    "grievous",
    instructions=(
        "Grievous is a hallucination engine. "
        "It generates typed pseudorandom data by asking an LLM to hallucinate it. "
        "Output is plausible, not guaranteed. No determinism. No schema validation. "
        "The footgun is yours."
    ),
)


@mcp.tool()
def generate(
    schema: str,
    count: int = 1,
    model: str = DEFAULT_MODEL,
) -> object:
    """
    Generate pseudorandom typed data by hallucinating it via Anthropic API.

    Args:
        schema:  Natural language or JSON schema description of what to generate.
                 e.g. "a User with name, age, email"
                 or   '{"type": "object", "properties": {"x": {"type": "number"}}}'
                 or   "a 4x4 float32 tensor"
        count:   Number of instances to generate. Default 1.
        model:   Anthropic model. Default claude-haiku-4-5-20251001.

    Returns:
        Parsed JSON if the model cooperated. Raw string if it didn't.
        No guarantees. Trigger discipline required.
    """
    return _generate(schema=schema, count=count, model=model)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
