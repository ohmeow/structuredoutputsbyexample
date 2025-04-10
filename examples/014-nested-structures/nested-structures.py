# Simple Nested Structure
# This example shows how to work with nested objects in Instructor.

import instructor
from openai import OpenAI
from pydantic import BaseModel

# Define nested data structure
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # Nested object

# Setup client
client = instructor.from_openai(OpenAI())

# Extract nested data
person = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": """
        John Smith is 35 years old and lives at
        123 Main Street, New York, 10001.
        """}
    ]
)

# Access nested data
# Output:
# Name: John Smith
# Age: 35
# Street: 123 Main Street
# City: New York
# ZIP: 10001
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Street: {person.address.street}")
print(f"City: {person.address.city}")
print(f"ZIP: {person.address.zip_code}")
