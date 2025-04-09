# Cohere Integration

# Use Instructor with Cohere's models for structured data extraction.
## pip install instructor cohere#
import instructor
import cohere
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Create Cohere client
co = cohere.Client("YOUR_API_KEY")  # or set CO_API_KEY env variable

# Patch with instructor
client = instructor.from_cohere(co)

# Using chat method
user = client.chat.completions.create(
    model="command-r-plus",  # or other Cohere models
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

print(f"Name: {user.name}, Age: {user.age}")
# Output: Name: John, Age: 25

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

user = client.chat.completions.create(
    model="command-r-plus",
    temperature=0.2,  # Lower for more consistent results
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

user = client.chat.completions.create(
    model="command-r-plus",
    response_model=User,
    preamble="You are an expert at extracting structured information.",
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

user = client.chat.completions.create(
    model="command-r-plus",
    response_model=User,
    messages=[
        {"role": "user", "content": "Hi, I'd like to discuss John who is 25 years old."},
        {"role": "assistant", "content": "Hello! I'd be happy to discuss John with you."},
        {"role": "user", "content": "Can you extract his information in a structured format?"}
    ]
)

# Default JSON mode
client = instructor.from_cohere(co)

# Explicit JSON mode
client = instructor.from_cohere(
    co,
    mode=instructor.Mode.JSON
)

