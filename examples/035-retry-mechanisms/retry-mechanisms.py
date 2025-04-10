# Retry Mechanisms
# Learn how to build robust extraction pipelines with automatic retry mechanisms in Instructor. This guide covers basic retry configuration, advanced retry strategies, and fallback mechanisms.
# Language models occasionally produce outputs that fail validation, especially with complex schemas or strict validation rules.
# Instructor's retry mechanisms enable graceful handling of validation failures to create more reliable and robust applications.

# Import necessary libraries
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator
from tenacity import Retrying, stop_after_attempt, wait_fixed
from instructor.exceptions import InstructorRetryException

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Basic retry configuration example
class Profile(BaseModel):
    username: str = Field(description="Username without spaces")
    age: int = Field(description="Age in years", ge=13)

    @field_validator("username")
    def validate_username(cls, v):
        if " " in v:
            raise ValueError("Username cannot contain spaces")
        return v

# Basic retry approach - specify max_retries
profile = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract: username: John Doe, age: 25"
        }
    ],
    response_model=Profile,
    max_retries=3  # Try up to 3 more times if validation fails
)

print("Basic retry example:")
print(profile.model_dump_json(indent=2))

# Advanced retry configuration with Tenacity
class User(BaseModel):
    name: str
    age: int

    @field_validator("name")
    def validate_name(cls, v):
        if not v.isupper():
            raise ValueError("Name must be uppercase")
        return v

# Use tenacity for advanced retry configuration
user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract: John is 30 years old"
        }
    ],
    response_model=User,
    max_retries=Retrying(
        stop=stop_after_attempt(3),  # Stop after 3 attempts
        wait=wait_fixed(1),  # Wait 1 second between attempts
    )
)

print("\nAdvanced retry with Tenacity:")
print(user.model_dump_json(indent=2))

# Handling persistent failures with fallback strategies
class ImpossibleModel(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def validate_age(cls, v):
        raise ValueError("This validator will always fail")

# Handle retry exceptions
try:
    print("\nTrying a model that will always fail validation:")
    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Extract: Jane is 25 years old"
            }
        ],
        response_model=ImpossibleModel,
        max_retries=2
    )
except InstructorRetryException as e:
    print(f"Failed after {e.n_attempts} attempts")
    print(f"Last error message: {e.messages[-1]['content']}")

    # Implement fallback strategy here
    fallback_result = {"name": "Jane", "age": 0}
    print(f"Using fallback: {fallback_result}")

# Retry best practices
print("\nRetry Best Practices:")
print("1. Start with a reasonable max_retries value (2-3 is often sufficient)")
print("2. Include clear validation error messages to guide the model")
print("3. Implement fallback strategies for handling persistent failures")
print("4. Use Tenacity for more advanced retry control (exponential backoff, etc.)")
print("5. Log validation errors to identify common failure patterns")
print("6. Consider adding system prompts that explain validation requirements")

