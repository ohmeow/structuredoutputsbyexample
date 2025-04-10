# Understanding Response Models
# Learn how to define effective Pydantic models for structuring LLM outputs with Instructor. This guide covers model creation, field validation, and descriptive hints.
# Unstructured LLM outputs can be difficult to validate and integrate into applications.
# Pydantic models provide a powerful way to define expected data structures and enforce validation rules.

# Import necessary libraries
from typing import List, Optional
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

# Simple model example
class User(BaseModel):
    name: str
    age: int

# Nested model example
class Address(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    country: str

class UserWithAddresses(BaseModel):
    name: str
    age: int
    addresses: List[Address]

# Model with field descriptions to guide the LLM
class WeatherForecast(BaseModel):
    """Weather forecast for a specific location"""

    temperature: float = Field(
        description="Current temperature in Celsius"
    )
    condition: str = Field(
        description="Weather condition (sunny, cloudy, rainy, etc.)"
    )
    humidity: int = Field(
        description="Humidity percentage from 0-100"
    )

# Model with validation constraints
class Product(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)  # greater than 0
    quantity: int = Field(ge=0)  # greater than or equal to 0
    description: str = Field(max_length=500)

# Initialize the client
client = instructor.from_openai(OpenAI())

# Extract structured data
forecast = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=WeatherForecast,
    messages=[
        {"role": "user", "content": "What's the weather in New York today?"}
    ]
)

print(forecast.model_dump_json(indent=2))

