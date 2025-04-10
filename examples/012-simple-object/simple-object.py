# Simple Object Extraction

# Extract basic objects from text with Instructor.
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    occupation: str

import instructor
from openai import OpenAI

# Patch the client
client = instructor.from_openai(OpenAI())

# Extract the data
person = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": "John Doe is a 30-year-old software engineer."}
    ]
)

print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Occupation: {person.occupation}")

# Output:# Name: John Doe# Age: 30# Occupation: software engineer

extracted = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": """
        In our company blog post, we want to highlight one of our newest team members.
        John Smith joined us last month. He's 34 years old and works as a data scientist.
        John previously worked at TechCorp for 5 years.
        """}
    ]
)

print(f"Name: {extracted.name}")
print(f"Age: {extracted.age}")
print(f"Occupation: {extracted.occupation}")

# Output:# Name: John Smith# Age: 34# Occupation: data scientist

from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")
    occupation: str = Field(description="The person's current job title or role")

extracted = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": """
        Meet Sarah Johnson, one of our senior architects.
        She's been with the firm since she was 28, and now at 42,
        she leads our sustainable design initiatives.
        """}
    ]
)

print(f"Name: {extracted.name}")
print(f"Age: {extracted.age}")
print(f"Occupation: {extracted.occupation}")

# Output:# Name: Sarah Johnson# Age: 42# Occupation: senior architect

class Employee(BaseModel):
    """Extract employee information from the provided text."""

    name: str
    age: int
    department: str
    years_of_service: int

extracted = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Employee,
    messages=[
        {"role": "user", "content": """
        Employee Profile: Michael Chen has been in our Marketing department for 7 years.
        He's 36 years old and has led multiple successful campaigns.
        """}
    ]
)

print(f"Name: {extracted.name}")
print(f"Department: {extracted.department}")
print(f"Years of Service: {extracted.years_of_service}")

# Output:# Name: Michael Chen# Department: Marketing# Years of Service: 7

