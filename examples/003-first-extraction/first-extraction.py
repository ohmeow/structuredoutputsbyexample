# Your First Extraction

# Create your first structured extraction with Instructor. Learn the step-by-step process from model definition to validated response.

# Extract structured data from text using Instructor and a Pydantic model.
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

import instructor
from openai import OpenAI

# Patch the client
client = instructor.from_openai(OpenAI())

# Extract structured data
person = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": "John Doe is 30 years old"}
    ]
)

print(f"Name: {person.name}, Age: {person.age}")
# Output: Name: John Doe, Age: 30

