# Getting Started with Structured Outputs

# Learn the basics of structured LLM outputs with Instructor. This guide demonstrates how to extract consistent, validated data from language models.

# Large language models (LLMs) are powerful tools for generating text, but extracting specific structured information from their outputs can be challenging. **Structured outputs** solve this problem by having LLMs return data in consistent, machine-readable formats rather than free-form text.
# 
# 
# 
# When working with LLMs, there are several issues with unstructured responses:
# Using a standard OpenAI client for unstructured output
from openai import OpenAI
client = OpenAI()

# Ask for customer information in free text
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Extract customer: John Doe, age 35, email: john@example.com"}
    ]
)

print(response.choices[0].message.content)
# Output might be:
# "Customer information:
# Name: John Doe
# Age: 35
# Email: john@example.com"

# This approach has several problems:
# 
# - **Inconsistent formats**: The LLM might return data in different formats each time
# - **Parsing challenges**: You need custom code to extract specific fields
# - **No validation**: There's no verification that the data is complete or correctly formatted
# - **Error handling**: Missing or invalid data is difficult to detect and manage
# 
# 
# 
# Instructor solves these problems by combining the power of LLMs with structured data validation through Pydantic:
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
        {"role": "user", "content": "Extract customer: John Doe, age 35, email: john@example.com"}
    ],
    response_model=Customer  # This is the key part
)

print(customer)  # Customer(name='John Doe', age=35, email='john@example.com')
print(f"Name: {customer.name}, Age: {customer.age}, Email: {customer.email}")

# 1. **Type Safety**: Get properly typed Python objects instead of raw strings
# 2. **Validation**: Automatic validation with detailed error messages
# 3. **Self-documenting**: Models clearly define the expected data structure
# 4. **Consistent Results**: Reliable, consistent data format across requests
# 5. **Error Handling**: Automatic retry with informative feedback when validation fails
# 6. **IDE Support**: Full autocomplete and type checking in your code editor
# 
# 
# 
# Instructor works by:
# 
# 1. Defining your expected data structure as a Pydantic model
# 2. Instructing the LLM to return data in a specific format (JSON, function calls, etc.)
# 3. Validating the response against your model
# 4. Automatically retrying if validation fails, providing the error to the LLM
# 5. Returning a properly typed Python object
# 
# 
# 
# Structured outputs shine for complex data:
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
        {"role": "user", "content": """
        Extract detailed information for this person:
        John Smith is a 42-year-old software engineer living at 123 Main St, San Francisco, CA 94105.
        His email is john.smith@example.com and phone is 555-123-4567.
        John is skilled in Python, JavaScript, and cloud architecture.
        """}
    ],
    response_model=Person
)

# Now you have a fully structured object
print(f"Name: {person.name}")
print(f"Location: {person.address.city}, {person.address.state}")
print(f"Skills: {', '.join(person.skills)}")

