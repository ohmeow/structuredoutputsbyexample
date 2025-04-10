# Custom Validators
# Learn how to implement custom validators for domain-specific validation rules with Instructor. This guide covers field validators, annotated validators, and LLM-based validation.
# Standard validation can address basic type checking and simple constraints, but many applications require more complex validation logic.
# Custom validators enable enforcing domain-specific rules, business logic, and contextual validation for more reliable data extraction.

# Import necessary libraries
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator, BeforeValidator, AfterValidator
from typing_extensions import Annotated
from instructor import llm_validator

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Basic custom field validators example
class Contact(BaseModel):
    name: str = Field(description="Person's full name")
    email: str = Field(description="Person's email address")
    phone: str = Field(description="Person's phone number")

    @field_validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Email must contain @ symbol")
        return v

    @field_validator("phone")
    def validate_phone(cls, v):
        # Remove all non-numeric characters
        digits = ''.join(c for c in v if c.isdigit())
        if len(digits) < 10:
            raise ValueError("Phone number must have at least 10 digits")
        return v

# Extract contact information with validation
contact = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract: John Doe, email: johndoe.example.com, phone: 555-1234"
        }
    ],
    response_model=Contact,
    max_retries=2
)

print("Custom validator example:")
print(contact.model_dump_json(indent=2))

# Annotated validation example
# Define a validation function
def validate_uppercase(v: str) -> str:
    if v != v.upper():
        raise ValueError("String must be uppercase")
    return v

# Define a model with annotated validation
class Document(BaseModel):
    title: Annotated[str, AfterValidator(validate_uppercase)]
    content: str

    @field_validator("content")
    def validate_content_length(cls, v):
        if len(v.split()) < 5:
            raise ValueError("Content must be at least 5 words long")
        return v

# Test document with annotated validation
document = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract: title: document title, content: This is too short."
        }
    ],
    response_model=Document,
    max_retries=2
)

print("\nAnnotated validator example:")
print(document.model_dump_json(indent=2))

# LLM-based validation example
class Review(BaseModel):
    product: str
    content: Annotated[
        str,
        BeforeValidator(llm_validator("must be positive and respectful", client=client))
    ]
    rating: int

# Example usage with LLM-based validator
review = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract: iPhone 14, content: This product is terrible and I hate it, rating: 1"
        }
    ],
    response_model=Review,
    max_retries=2
)

print("\nLLM-based validator example:")
print(review.model_dump_json(indent=2))

# Note: The LLM validator will transform the negative review into a more positive and respectful one
print("\nLLM-based validators can intelligently transform invalid data to make it valid.")
print("This is powerful for complex validation where simple rules aren't sufficient.")
print("Examples include ensuring content is professional, factual, or meets specific guidelines.")

