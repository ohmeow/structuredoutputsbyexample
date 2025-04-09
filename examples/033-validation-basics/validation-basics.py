# Validation Basics

# 4. The process repeats until validation passes or max retries is reached

# Instructor leverages Pydantic's validation framework to ensure that outputs from LLMs match your expected schema. This is crucial for building reliable applications.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

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

# Example usage
text = "John Doe is 25 years old and his email is john.doe@example.com."
user = extract_user(text)
print(user.model_dump_json(indent=2))

# When an LLM output fails validation, Instructor can automatically retry the request with the validation error message:
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with custom validation
class User(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError("Age must be between 0 and 120")
        return v

# Extract with automatic retries
user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract: John Doe, age: 150"
        }
    ],
    response_model=User,
    max_retries=2  # Try up to 2 more times if validation fails
)

print(user.model_dump_json(indent=2))

