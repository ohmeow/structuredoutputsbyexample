# Getting Started with Structured Outputs

# Learn the basics of structured LLM outputs with Instructor. This guide demonstrates how to extract consistent, validated data from language models.

# Large language models are powerful, but extracting structured data can be challenging.
# Structured outputs solve this by having LLMs return data in consistent, machine-readable formats.

# Using a standard OpenAI client for unstructured output
from openai import OpenAI

client = OpenAI()

# Ask for customer information in free text
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract customer: John Doe, age 35, email: john@example.com",
        }
    ],
)

print(response.choices[0].message.content)

# Instructor solves these problems by combining LLMs with Pydantic validation:
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, EmailStr


# Define a structured data model
class Customer(BaseModel):
    name: str = Field(description="Customer's full name")
    age: int = Field(description="Customer's age in years", ge=0, le=120)
    email: EmailStr = Field(description="Customer's email address")


# Patch the OpenAI client with Instructor
client = instructor.from_openai(OpenAI())

# Extract structured customer data
customer = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract customer: John Doe, age 35, email: john@example.com",
        }
    ],
    response_model=Customer,  # This is the key part
)

print(customer)  # Customer(name='John Doe', age=35, email='john@example.com')
print(f"Name: {customer.name}, Age: {customer.age}, Email: {customer.email}")

# Benefits:# - Type Safety: Properly typed Python objects instead of raw strings# - Validation: Automatic validation with detailed error messages# - Self-documenting: Models clearly define the expected data structure# - Consistent Results: Reliable data format across requests# - Error Handling: Automatic retry with informative feedback

# Instructor workflow:# 1. Define your data structure as a Pydantic model# 2. Instruct the LLM to return data in a specific format# 3. Validate the response against your model# 4. Automatically retry if validation fails# 5. Return a properly typed Python object

# Complex data example:
from typing import List, Optional
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())


# Define a complex, nested data structure
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class Contact(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None


class Person(BaseModel):
    name: str
    age: int
    occupation: str
    address: Address
    contact: Contact
    skills: List[str] = Field(description="List of professional skills")


# Extract structured data
person = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": """
        Extract detailed information for this person:
        John Smith is a 42-year-old software engineer living at 123 Main St, San Francisco, CA 94105.
        His email is john.smith@example.com and phone is 555-123-4567.
        John is skilled in Python, JavaScript, and cloud architecture.
        """,
        }
    ],
    response_model=Person,
)

# Now you have a fully structured object
print(f"Name: {person.name}")
print(f"Location: {person.address.city}, {person.address.state}")
print(f"Skills: {', '.join(person.skills)}")
