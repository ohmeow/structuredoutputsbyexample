# List Extraction
# You are also able to extract lists of objects from text with Instructor.

# Extract multiple items in a list from text with Instructor.
from pydantic import BaseModel
import instructor
from openai import OpenAI
from typing import List

# Define the Person class with Pydantic
class Person(BaseModel):
    name: str
    age: int


# Patch the client
client = instructor.from_openai(OpenAI())

# Extract a list of people
people = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=List[Person],  # Note the List wrapper
    messages=[
        {"role": "user", "content": """
        Extract all people mentioned in this text:
        - John is 30 years old
        - Mary is 25 years old
        - Bob is 45 years old
        """}
    ]
)

# Print each person
# Expected output:
# John is 30 years old
# Mary is 25 years old
# Bob is 45 years old
for person in people:
    print(f"{person.name} is {person.age} years old")