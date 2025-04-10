# OpenAI Integration

# Instructor works seamlessly with OpenAI models. Here's how to use it with different OpenAI features.
import instructor
from openai import OpenAI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

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

# Instructor defaults to using OpenAI's function calling format, but you can use JSON mode too:
client = instructor.from_openai(
    OpenAI(),
    mode=instructor.Mode.JSON
)

user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is a 25-year-old engineer."}
    ]
)

import asyncio
from openai import AsyncOpenAI

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

