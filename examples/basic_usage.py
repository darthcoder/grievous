"""Basic usage: generate a single object from a natural-language schema."""
from grievous.backend import generate

user = generate("a User with name, age, email, and city")
print(user)
