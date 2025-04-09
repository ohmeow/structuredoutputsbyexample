# Fallback Strategies

# - Default values for missing information

# When working with LLMs, it's important to have fallback strategies for handling persistent failures or unexpected issues. Instructor provides several ways to implement robust fallback mechanisms.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from instructor.exceptions import InstructorRetryException

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define primary model with strict validation
class DetailedUserProfile(BaseModel):
    name: str = Field(description="User's full name")
    age: int = Field(description="User's age in years", ge=18)
    occupation: str = Field(description="User's job or profession")
    income: int = Field(description="User's annual income in USD", ge=0)
    education: str = Field(description="User's highest education level")

# Define simpler fallback model
class BasicUserProfile(BaseModel):
    name: str = Field(description="User's name")
    age: int = Field(description="User's age", ge=0)

# Try extraction with fallback strategy
def extract_user_with_fallback(text: str):
    try:
        # First attempt with detailed model
        return client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Extract user information: {text}"
                }
            ],
            response_model=DetailedUserProfile,
            max_retries=2
        )
    except InstructorRetryException:
        print("Detailed extraction failed, falling back to basic profile")
        # Fall back to simpler model
        return client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Extract basic user information: {text}"
                }
            ],
            response_model=BasicUserProfile,
            max_retries=1
        )

# Example usage
text = "John is 25 years old"
user = extract_user_with_fallback(text)
print(user.model_dump_json(indent=2))

# Another approach is to use optional fields for less reliable information:
from typing import Optional
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define model with optional fields
class FlexibleProfile(BaseModel):
    name: str = Field(description="Person's name")
    age: Optional[int] = Field(None, description="Person's age if mentioned")
    location: Optional[str] = Field(None, description="Person's location if mentioned")
    occupation: Optional[str] = Field(None, description="Person's job if mentioned")

# Extract what's available without failing
profile = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Sarah is a software engineer from Boston"
        }
    ],
    response_model=FlexibleProfile
)

print(profile.model_dump_json(indent=2))

# For critical applications, you can implement a more comprehensive fallback strategy:
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from enum import Enum

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define extraction result status
class ExtractionStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"

# Define target model
class Contact(BaseModel):
    name: str
    email: str
    phone: str

# Define wrapper for extraction result
class ExtractionResult(BaseModel):
    status: ExtractionStatus
    data: dict
    error_message: str = ""

# Robust extraction function with fallbacks
def extract_with_robustness(text: str) -> ExtractionResult:
    try:
        # Primary extraction attempt
        result = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Extract contact info: {text}"}],
            response_model=Contact,
            max_retries=2
        )
        return ExtractionResult(
            status=ExtractionStatus.SUCCESS,
            data=result.model_dump()
        )
    except InstructorRetryException as e:
        # Attempt partial extraction
        try:
            partial_data = {}
            # Parse the error message
            error_msg = e.messages[-1]["content"]

            # Try to salvage whatever fields we can
            text_lines = text.split('\n')
            for line in text_lines:
                if "name:" in line.lower():
                    partial_data["name"] = line.split("name:")[1].strip()
                if "email:" in line.lower():
                    partial_data["email"] = line.split("email:")[1].strip()
                if "phone:" in line.lower():
                    partial_data["phone"] = line.split("phone:")[1].strip()

            if partial_data:
                return ExtractionResult(
                    status=ExtractionStatus.PARTIAL,
                    data=partial_data,
                    error_message=error_msg
                )
            else:
                return ExtractionResult(
                    status=ExtractionStatus.FAILED,
                    data={},
                    error_message=error_msg
                )
        except Exception as nested_error:
            return ExtractionResult(
                status=ExtractionStatus.FAILED,
                data={},
                error_message=f"Complete extraction failure: {str(nested_error)}"
            )

