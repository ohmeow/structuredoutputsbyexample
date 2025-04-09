# Understanding Response Models

# 

# Instructor uses Pydantic models to define the structure of your LLM outputs. Here's how to create effective models.
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    country: str

class User(BaseModel):
    name: str
    age: int
    addresses: List[Address]

# Add descriptions to help guide the LLM:
from pydantic import BaseModel, Field

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

# Add validation constraints to ensure quality data:
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)  # greater than 0
    quantity: int = Field(ge=0)  # greater than or equal to 0
    description: str = Field(max_length=500)

import instructor
from openai import OpenAI

client = instructor.from_openai(OpenAI())

forecast = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=WeatherForecast,
    messages=[
        {"role": "user", "content": "What's the weather in New York today?"}
    ]
)

print(forecast.model_dump_json(indent=2))

