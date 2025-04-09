# Mistral Integration

# 

# Use Instructor with Mistral AI models for structured data extraction.
# 
# 
# 
# 
# 
# pip install instructor mistralai
# 
import instructor
from mistralai.client import MistralClient
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Create Mistral client
mistral_client = MistralClient(api_key="YOUR_API_KEY")

# Patch with instructor
client = instructor.from_mistral(mistral_client)

# Using chat method
user = client.chat.completions.create(
    model="mistral-large-latest",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

print(f"Name: {user.name}, Age: {user.age}")
# Output: Name: John, Age: 25

# Mistral Small
user = client.chat.completions.create(
    model="mistral-small-latest",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

# Mistral Medium
user = client.chat.completions.create(
    model="mistral-medium-latest",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

# Mistral Large (most capable)
user = client.chat.completions.create(
    model="mistral-large-latest",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

user = client.chat.completions.create(
    model="mistral-large-latest",
    response_model=User,
    messages=[
        {"role": "system", "content": "You are an expert at data extraction."},
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

user = client.chat.completions.create(
    model="mistral-large-latest",
    temperature=0.2,  # Lower for more consistent results
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

user = client.chat.completions.create(
    model="mistral-large-latest",
    response_model=User,
    messages=[
        {"role": "user", "content": "Hi, I'd like to discuss John who is 25 years old."},
        {"role": "assistant", "content": "Hello! I'd be happy to discuss John with you."},
        {"role": "user", "content": "Can you extract his information in a structured format?"}
    ]
)

# Default JSON mode
client = instructor.from_mistral(mistral_client)

# Explicit JSON mode
client = instructor.from_mistral(
    mistral_client,
    mode=instructor.Mode.JSON
)

# Using MD_JSON mode
client = instructor.from_mistral(
    mistral_client,
    mode=instructor.Mode.MD_JSON
)

import asyncio
from mistralai.async_client import MistralAsyncClient

async_client = instructor.from_mistral(
    MistralAsyncClient(api_key="YOUR_API_KEY")
)

async def extract_user():
    return await async_client.chat.completions.create(
        model="mistral-large-latest",
        response_model=User,
        messages=[
            {"role": "user", "content": "Extract: John is 25 years old."}
        ]
    )

user = asyncio.run(extract_user())

