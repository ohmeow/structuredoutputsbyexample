# List Extraction
# Learn how to extract multiple items in a list from text using Instructor. This guide covers basic list extraction, complex nested structures, and streaming extraction.
# Real-world data often contains multiple items of the same type that need to be extracted together.
# Instructor makes it easy to extract lists of structured data with proper typing and validation.

# Import necessary libraries
import instructor
from openai import OpenAI
from typing import List, Optional
from pydantic import BaseModel, Field

# Define a simple model for extraction
class Person(BaseModel):
    name: str
    age: int

# Patch the client
client = instructor.from_openai(OpenAI())

# Basic list extraction example
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
for person in people:
    print(f"{person.name} is {person.age} years old")
# Output:
# John is 30 years old
# Mary is 25 years old
# Bob is 45 years old

# Extracting from natural language text
people = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=List[Person],
    messages=[
        {"role": "user", "content": """
        Our team has grown significantly this year. John Smith, who is 32, joined our
        engineering department. We also welcomed Sarah Johnson, 28, to our design team.
        The most recent addition is Michael Chen, who is 35 and brings valuable experience.
        """}
    ]
)

for i, person in enumerate(people, 1):
    print(f"Person {i}: {person.name}, {person.age}")
# Output:
# Person 1: John Smith, 32
# Person 2: Sarah Johnson, 28
# Person 3: Michael Chen, 35

# Complex list extraction with nested structures
class Address(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    country: str

class PersonWithAddresses(BaseModel):
    name: str
    age: int
    occupation: str = Field(description="The person's job or profession")
    addresses: List[Address] = Field(description="List of addresses associated with this person")

people = client.chat.completions.create(
    model="gpt-4",  # More complex extraction works better with more capable models
    response_model=List[PersonWithAddresses],
    messages=[
        {"role": "user", "content": """
        Our company employees include:

        1. John Smith is a 34-year-old software developer who lives at 123 Main St, Boston, USA
           and has a vacation home at 456 Beach Road, Miami, USA.

        2. Maria Garcia is 29 and works as a marketing specialist. She lives at
           78 Park Avenue, New York, USA.

        3. Ahmed Hassan, 41, is our senior data scientist who recently moved from
           555 River St, Cairo, Egypt to 890 Tech Blvd, San Francisco, USA.
        """}
    ]
)

for person in people:
    print(f"{person.name}, {person.age} - {person.occupation}")
    for i, addr in enumerate(person.addresses, 1):
        print(f"  Address {i}: {addr.street}, {addr.city}, {addr.country}")
    print()

# Streaming list extraction
# Extract with streaming using create_iterable
people_stream = client.chat.completions.create_iterable(
    model="gpt-3.5-turbo",
    response_model=Person,  # Note: no List wrapper here
    messages=[
        {"role": "user", "content": """
        Extract all people mentioned in this text:
        - John is 30 years old
        - Mary is 25 years old
        - Bob is 45 years old
        """}
    ]
)

# Process each item as it's completed
for person in people_stream:
    print(f"Received: {person.name} is {person.age} years old")
# Output will appear one at a time as each is completed:
# Received: John is 30 years old
# Received: Mary is 25 years old
# Received: Bob is 45 years old

