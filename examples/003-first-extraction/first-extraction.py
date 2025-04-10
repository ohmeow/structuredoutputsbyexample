# Your First Extraction
# Create your first structured extraction with Instructor. Learn the step-by-step process from model definition to validated response.
# Traditional LLM responses are unstructured and difficult to integrate with applications.
# Instructor simplifies this by enabling structured extractions with type safety and validation.

# Import necessary libraries
from pydantic import BaseModel
import instructor
from openai import OpenAI

# Define a Pydantic model for the structured output
class Person(BaseModel):
    name: str
    age: int

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

# Output: Name: John Doe, Age: 30
print(f"Name: {person.name}, Age: {person.age}")

