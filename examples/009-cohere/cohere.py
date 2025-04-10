# Cohere Integration
# Learn how to use Instructor with Cohere's models for structured data extraction. This guide covers model selection, parameters, and conversation handling.
# Cohere provides powerful language models with a focus on enterprise applications.
# Instructor makes it easy to extract structured data from Cohere models with type safety and validation.

# Import necessary libraries
import instructor
import cohere
from pydantic import BaseModel

# Define a simple model for extraction
class User(BaseModel):
    name: str
    age: int

# Create Cohere client
co = cohere.Client("YOUR_API_KEY")  # or set CO_API_KEY env variable

# Patch with instructor - default JSON mode
client = instructor.from_cohere(co)

# Basic extraction example
user = client.chat.completions.create(
    model="command-r-plus",  # or other Cohere models
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

print(f"Name: {user.name}, Age: {user.age}")
# Output: Name: John, Age: 25

# Different model options
# Command model
user = client.chat.completions.create(
    model="command",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

# Command R model
user = client.chat.completions.create(
    model="command-r",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

# Command R+ model (most capable)
user = client.chat.completions.create(
    model="command-r-plus",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

# Using temperature to control randomness
user = client.chat.completions.create(
    model="command-r-plus",
    temperature=0.2,  # Lower for more consistent results
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

# Using preamble (similar to system message)
user = client.chat.completions.create(
    model="command-r-plus",
    response_model=User,
    preamble="You are an expert at extracting structured information.",
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

# Multi-turn conversation
user = client.chat.completions.create(
    model="command-r-plus",
    response_model=User,
    messages=[
        {"role": "user", "content": "Hi, I'd like to discuss John who is 25 years old."},
        {"role": "assistant", "content": "Hello! I'd be happy to discuss John with you."},
        {"role": "user", "content": "Can you extract his information in a structured format?"}
    ]
)

# Client configurations
# Default JSON mode
default_client = instructor.from_cohere(co)

# Explicit JSON mode
json_client = instructor.from_cohere(
    co,
    mode=instructor.Mode.JSON
)

