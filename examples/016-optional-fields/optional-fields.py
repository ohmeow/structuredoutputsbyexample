# Optional Fields
# This example demonstrates how to handle optional or missing data in structured extractions:
# 1. Using Optional type annotations for fields that might not be present in the source text
# 2. Using Instructor's Maybe type to explicitly track whether information was present
#
# Optional fields allow your models to gracefully handle incomplete information without
# causing extraction failures when certain data isn't mentioned in the text.

# Import the necessary libraries
from pydantic import BaseModel, Field
from typing import Optional
import instructor
from openai import OpenAI

# Define the Person class with Pydantic
class Person(BaseModel):
    name: str
    age: int
    # Optional fields with default value of None
    email: Optional[str] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None

# Patch the client
client = instructor.from_openai(OpenAI())

# Extract with optional fields
person = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": "John Smith is 35 years old and works as a software engineer."}
    ]
)

# Output:
# Name: John Smith
# Age: 35
# Email: None
# Phone: None
# Occupation: software engineer
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Email: {person.email}")  # None
print(f"Phone: {person.phone}")  # None
print(f"Occupation: {person.occupation}")  # "software engineer"
