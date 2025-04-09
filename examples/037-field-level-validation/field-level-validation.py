# Field-level Validation

# Apply field-level validation rules to enforce domain-specific business logic. Instructor allows fine-grained control over data validation.

# Instructor supports detailed field-level validation to ensure that specific parts of the LLM output meet your requirements. This allows for fine-grained control over the extracted data.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator
import re

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with field-level validation
class UserProfile(BaseModel):
    username: str = Field(
        description="Username (lowercase, no spaces)",
        min_length=3,
        max_length=20
    )
    email: str = Field(
        description="Valid email address"
    )
    age: int = Field(
        description="Age in years",
        ge=13,  # Greater than or equal to 13
        le=120  # Less than or equal to 120
    )

    @field_validator("username")
    def validate_username(cls, v):
        if not v.islower() or " " in v:
            raise ValueError("Username must be lowercase and contain no spaces")
        return v

    @field_validator("email")
    def validate_email(cls, v):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v

# Extract user profile with validation
profile = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract user profile: John Doe, john.doe@example.com, 25 years old"
        }
    ],
    response_model=UserProfile,
    max_retries=2
)

print(profile.model_dump_json(indent=2))

# You can also use Pydantic's Field parameters for basic constraints:
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with Field constraints
class Product(BaseModel):
    name: str = Field(
        description="Product name",
        min_length=2,
        max_length=100
    )
    price: float = Field(
        description="Product price in USD",
        gt=0  # Greater than 0
    )
    description: str = Field(
        description="Product description",
        min_length=10,
        max_length=1000
    )
    tags: List[str] = Field(
        description="Product tags",
        min_length=1,  # At least one tag
        max_length=10  # At most 10 tags
    )

# Example usage
product = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract product info: iPhone, $999, Latest smartphone with advanced features, tags: electronics, smartphone, apple"
        }
    ],
    response_model=Product
)

print(product.model_dump_json(indent=2))

# For more complex validation, you can use annotated types:
from typing_extensions import Annotated
from pydantic import AfterValidator
import re

def validate_phone_number(v: str) -> str:
    """Validate phone number format."""
    # Remove all non-numeric characters
    digits = ''.join(c for c in v if c.isdigit())
    if len(digits) < 10:
        raise ValueError("Phone number must have at least 10 digits")
    return v

def validate_zip_code(v: str) -> str:
    """Validate US zip code format."""
    pattern = r"^\d{5}(-\d{4})?$"
    if not re.match(pattern, v):
        raise ValueError("Invalid zip code format (must be 12345 or 12345-6789)")
    return v

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: Annotated[str, AfterValidator(validate_zip_code)]
    phone: Annotated[str, AfterValidator(validate_phone_number)]

