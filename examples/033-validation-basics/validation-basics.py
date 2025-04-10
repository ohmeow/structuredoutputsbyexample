# Validation Basics
# Learn the fundamentals of validation in Instructor. This guide explains the automatic validation and retry process for ensuring data quality in structured extractions.
# Unstructured outputs from language models often contain errors, inconsistencies, or invalid data formats.
# Instructor leverages Pydantic's validation framework to ensure that LLM outputs match your expected schema, making applications more reliable.

# Import necessary libraries
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with basic validation
class User(BaseModel):
    name: str = Field(..., description="User's full name")
    age: int = Field(...,
                    description="User's age in years",
                    ge=0, le=120)  # Must be between 0 and 120
    email: str = Field(..., description="User's email address")

# Extract user information with validation
def extract_user(text: str) -> User:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Extract user information from this text: {text}"
            }
        ],
        response_model=User
    )

# Example usage with valid data
text = "John Doe is 25 years old and his email is john.doe@example.com."
user = extract_user(text)
print("Valid data extraction:")
print(user.model_dump_json(indent=2))

# Automatic retry with validation errors
# Define a model with custom validation
class UserWithCustomValidation(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError("Age must be between 0 and 120")
        return v

# Extract with automatic retries
user_retry = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract: John Doe, age: 150"
        }
    ],
    response_model=UserWithCustomValidation,
    max_retries=2  # Try up to 2 more times if validation fails
)

print("\nAfter automatic retry with validation error:")
print(user_retry.model_dump_json(indent=2))

# What happens during validation failures
print("\nValidation Process:")
print("1. LLM generates a response")
print("2. Instructor attempts to parse the response into the Pydantic model")
print("3. If validation fails, Instructor sends the error back to the LLM")
print("4. LLM generates a corrected response based on the error")
print("5. Process repeats until valid or max_retries is reached")

