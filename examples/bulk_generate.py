"""Generate a batch of records — useful for seeding a dev database."""
import json
from grievous.backend import generate

products = generate("a Product with id, name, price_usd, and category", count=10)
print(json.dumps(products, indent=2))
