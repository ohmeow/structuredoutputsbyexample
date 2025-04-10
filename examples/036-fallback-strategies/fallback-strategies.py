# Fallback Strategies
# Learn how to implement fallback strategies for handling missing or invalid information with Instructor. This guide covers multiple approaches to creating robust extraction pipelines.
# Even with retries, LLM extractions can sometimes fail due to ambiguous inputs, conflicting requirements, or genuinely missing information.
# Fallback strategies provide graceful degradation paths when primary extraction methods fail, ensuring your applications remain reliable.

# Import necessary libraries
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from instructor.exceptions import InstructorRetryException
from typing import Optional, Dict, Any
from enum import Enum

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Approach 1: Model hierarchy fallback
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
        return client.chat.completions.create(  # First attempt with detailed model
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
        return client.chat.completions.create(  # Fall back to simpler model
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
print("Approach 1: Model hierarchy fallback")
print(user.model_dump_json(indent=2))

# Approach 2: Optional fields for less reliable information
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

print("\nApproach 2: Optional fields")
print(profile.model_dump_json(indent=2))

# Approach 3: Comprehensive fallback strategy with status tracking
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
        result = client.chat.completions.create(  # Primary extraction attempt
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Extract contact info: {text}"}],
            response_model=Contact,
            max_retries=2
        )
        return ExtractionResult(
            status=ExtractionStatus.SUCCESS,
            data=result.model_dump()
        )
    # Attempt to salvage partial data when extraction fails
    except InstructorRetryException as e:
        try:
            partial_data = {}
            error_msg = e.messages[-1]["content"]  # Parse the error message
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

# Example with the robust extraction approach
contact_text = """
name: Alice Smith
email: alice@example
phone: incomplete
"""

result = extract_with_robustness(contact_text)
print("\nApproach 3: Comprehensive fallback with status tracking")
print(f"Status: {result.status}")
print(f"Data: {result.data}")
print(f"Error: {result.error_message}")

# Summary of fallback approaches
print("\nFallback Strategy Summary:")
print("1. Model Hierarchy: Fall back to simpler models when complex extraction fails")
print("2. Optional Fields: Use Optional types for information that might be missing")
print("3. Status Tracking: Return extraction status with partial results when possible")
print("4. Combining Approaches: Mix these strategies for maximum robustness")
print("5. Consider provider fallbacks: Try different models or even different LLM providers")

