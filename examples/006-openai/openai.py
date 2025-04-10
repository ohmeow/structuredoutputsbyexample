# OpenAI Integration
# Learn how to use Instructor with OpenAI's models for structured data extraction. This guide covers model selection, parameters, and async functionality.
# OpenAI offers various models with different capabilities and pricing tiers.
# Instructor works seamlessly with all OpenAI models, allowing you to choose the right one for your needs.

# Import necessary libraries
import instructor
import asyncio
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel

# Define a simple model for extraction
class User(BaseModel):
    name: str
    age: int

# Initialize the instructor-patched client
client = instructor.from_openai(OpenAI())

# GPT-3.5 Turbo (cheaper, faster)
user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is a 25-year-old engineer."}
    ]
)

# GPT-4 (more capable, better at complex tasks)
user = client.chat.completions.create(
    model="gpt-4",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is a 25-year-old engineer."}
    ]
)

# Using system messages to guide extraction
user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=User,
    messages=[
        {"role": "system", "content": "You are an expert at data extraction."},
        {"role": "user", "content": "Extract user details from: John is 25 years old."}
    ]
)

# Lower temperature for more consistent results
user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.1,  # Very deterministic (0.0-1.0)
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is a 25-year-old engineer."}
    ]
)

# Using JSON mode instead of function calling
json_client = instructor.from_openai(
    OpenAI(),
    mode=instructor.Mode.JSON
)

user = json_client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is a 25-year-old engineer."}
    ]
)

# Async client for non-blocking operations
async_client = instructor.from_openai(AsyncOpenAI())

async def extract_user():
    return await async_client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=User,
        messages=[
            {"role": "user", "content": "Extract: John is a 25-year-old engineer."}
        ]
    )

user = asyncio.run(extract_user())

