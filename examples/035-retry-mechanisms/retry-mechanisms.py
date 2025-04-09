# Retry Mechanisms

# - Creating robust production applications

# Instructor provides flexible retry mechanisms for handling validation failures. This helps create more robust applications that can recover from parsing errors or validation issues.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with validation
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

print(profile.model_dump_json(indent=2))

# For more advanced retry logic, you can use the Tenacity library:
import instructor
from openai import OpenAI
from pydantic import BaseModel, field_validator
from tenacity import Retrying, stop_after_attempt, wait_fixed

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with validation
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

print(user.model_dump_json(indent=2))

# You can also catch retry exceptions to handle persistent failures:
import instructor
from openai import OpenAI
from pydantic import BaseModel, field_validator
from instructor.exceptions import InstructorRetryException

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model with validation that will always fail
class ImpossibleModel(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def validate_age(cls, v):
        raise ValueError("This validator will always fail")

# Handle retry exceptions
try:
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

