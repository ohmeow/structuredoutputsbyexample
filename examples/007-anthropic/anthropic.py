# Anthropic Integration

# Use Instructor with Anthropic's Claude models for structured data extraction.
import instructor
from anthropic import Anthropic
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int


# Create patched client
client = instructor.from_anthropic(Anthropic())

# Claude 3 Haiku (faster, cheaper)
user = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    response_model=User,
    messages=[{"role": "user", "content": "Extract: John is 25 years old."}],
)

# Claude 3 Sonnet (balanced)
user = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1000,
    response_model=User,
    messages=[{"role": "user", "content": "Extract: John is 25 years old."}],
)

# Claude 3 Opus (most capable)
user = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    response_model=User,
    messages=[{"role": "user", "content": "Extract: John is 25 years old."}],
)

user = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    response_model=User,
    system="You are an expert at data extraction. Always extract all details accurately.",
    messages=[{"role": "user", "content": "Extract: John is 25 years old."}],
)

user = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    temperature=0.2,  # Lower temperature for more consistent results
    response_model=User,
    messages=[{"role": "user", "content": "Extract: John is 25 years old."}],
)

# Default: ANTHROPIC_TOOLS mode
client = instructor.from_anthropic(Anthropic())

# JSON mode
json_client = instructor.from_anthropic(Anthropic(), mode=instructor.Mode.JSON)

# Markdown JSON mode
md_client = instructor.from_anthropic(Anthropic(), mode=instructor.Mode.MD_JSON)

import asyncio
from anthropic import AsyncAnthropic

async_client = instructor.from_anthropic(AsyncAnthropic())


async def extract_user():
    return await async_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        response_model=User,
        messages=[{"role": "user", "content": "Extract: John is 25 years old."}],
    )


user = asyncio.run(extract_user())
