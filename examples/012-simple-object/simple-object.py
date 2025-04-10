# Simple Object Extraction
# Here we extract basic objects from text with Instructor

# Import the necessary libraries
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

# Define the Person class with Pydantic
class Person(BaseModel):
    """Extract person information from text."""
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")
    occupation: str = Field(description="The person's current job title or role")

# Patch the OpenAI client with Instructor
client = instructor.from_openai(OpenAI())

# Extract the data from text
person = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": "John Doe is a 30-year-old software engineer."}
    ]
)

# Print the extracted structured data
# Output:
# Name: John Doe
# Age: 30
# Occupation: software engineer
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Occupation: {person.occupation}")
