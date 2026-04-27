"""Use a JSON Schema string as the schema argument instead of natural language."""
import json
from grievous.backend import generate

schema = json.dumps({
    "type": "object",
    "properties": {
        "transaction_id": {"type": "string", "format": "uuid"},
        "amount_usd": {"type": "number"},
        "currency": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "status": {"type": "string", "enum": ["pending", "cleared", "failed"]},
    },
})

txn = generate(schema)
print(txn)
