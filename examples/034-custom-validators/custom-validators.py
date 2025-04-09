# Custom Validators

# - Context-dependent validation

# Instructor allows you to create custom validators to enforce specific rules on LLM outputs. These can range from simple format checks to complex business logic.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with a custom validator
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

print(contact.model_dump_json(indent=2))

# You can also use validation with annotated types:
from typing_extensions import Annotated
from pydantic import AfterValidator

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

# For even more advanced validation, you can use LLM-based validators:
import instructor
from openai import OpenAI
from pydantic import BaseModel, BeforeValidator
from typing_extensions import Annotated
from instructor import llm_validator

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with LLM-based validation
class Review(BaseModel):
    product: str
    content: Annotated[
        str,
        BeforeValidator(llm_validator("must be positive and respectful", client=client))
    ]
    rating: int

# Example usage
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

