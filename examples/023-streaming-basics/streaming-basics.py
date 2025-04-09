# Streaming Basics

# Get started with streaming responses in Instructor for real-time processing.
# 
# Streaming allows you to receive partial responses from LLMs as they're being generated, 
# rather than waiting for the complete response.
#
# Instructor offers two main ways to stream structured data:
# 
# 1. Partial: Stream a single object as it's being populated field by field
# 2. Iterable: Stream multiple complete objects one at a time
import instructor
from openai import OpenAI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    bio: str

# Patch the OpenAI client
client = instructor.from_openai(OpenAI())

def stream_user_info():
    # Create a streaming response
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=User,
        stream=True,  # Enable streaming
        messages=[
            {"role": "user", "content": "Generate a profile for a fictional user named Alice who is 28 years old."}
        ]
    )

    # Process the stream
    for chunk in stream:
        # The chunk contains a partial response so far
        print(f"Received chunk: {chunk}")

    # The last chunk is the complete response
    return chunk

user = stream_user_info()
print(f"\nFinal result: {user}")

from instructor import Partial

def stream_user_with_partial():
    # Create a streaming response using create_partial
    user_stream = client.chat.completions.create_partial(
        model="gpt-3.5-turbo",
        response_model=User,
        messages=[
            {"role": "user", "content": "Generate a profile for a fictional user named Bob who is 35 years old and works as a software developer."}
        ]
    )

    # Process the stream of Partial[User] objects
    print("Streaming user data:")

    for partial_user in user_stream:
        # As new fields are populated, they show up in the partial_user
        print(f"Current state: name={partial_user.name}, age={partial_user.age}, bio={partial_user.bio!r}")

# Example output:
# Current state: name=None, age=None, bio=None
# Current state: name='Bob', age=None, bio=None
# Current state: name='Bob', age=35, bio=None
# Current state: name='Bob', age=35, bio='Software developer with 10 years of experience...'

from typing import Dict, Any

class ProgressTracker:
    def __init__(self):
        self.progress = {}

    def update(self, partial_user: Partial[User]):
        # Calculate percentage of fields that are populated
        total_fields = len(User.model_fields)
        populated = sum(1 for v in [partial_user.name, partial_user.age, partial_user.bio] if v is not None)
        completion = int(populated / total_fields * 100)

        # Track changes
        data = {}
        if partial_user.name is not None:
            data["name"] = partial_user.name
        if partial_user.age is not None:
            data["age"] = partial_user.age
        if partial_user.bio is not None:
            data["bio"] = partial_user.bio

        self.progress = {
            "completion": f"{completion}%",
            "data": data
        }

        return self.progress

def stream_with_progress():
    tracker = ProgressTracker()

    user_stream = client.chat.completions.create_partial(
        model="gpt-3.5-turbo",
        response_model=User,
        messages=[
            {"role": "user", "content": "Generate a profile for a fictional user named Carol who is 42 years old."}
        ]
    )

    for partial_user in user_stream:
        progress = tracker.update(partial_user)
        print(f"Progress: {progress['completion']} - Current data: {progress['data']}")

# Example output:
# Progress: 33% - Current data: {'name': 'Carol'}
# Progress: 66% - Current data: {'name': 'Carol', 'age': 42}
# Progress: 100% - Current data: {'name': 'Carol', 'age': 42, 'bio': 'Carol is a passionate...'}

import asyncio
from openai import AsyncOpenAI

async def stream_async():
    # Create async client
    async_client = instructor.from_openai(AsyncOpenAI())

    # Create an async streaming response
    user_stream = await async_client.chat.completions.create_partial(
        model="gpt-3.5-turbo",
        response_model=User,
        messages=[
            {"role": "user", "content": "Generate a profile for a fictional user named Dave who is 31 years old."}
        ]
    )

    # Process the stream
    async for partial_user in user_stream:
        print(f"Async stream update: {partial_user}")

# Run the async function
asyncio.run(stream_async())

