# Other Provider Integrations

# 

# Instructor supports many LLM providers beyond the major ones. Here's a quick overview of some additional providers.
import instructor
from litellm import completion
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Patch LiteLLM completion function
client = instructor.from_litellm(completion)

# Use with any provider supported by LiteLLM
user = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or any other provider/model combination
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

import instructor
from pydantic import BaseModel
from vertexai.preview.generative_models import GenerativeModel

class User(BaseModel):
    name: str
    age: int

# Create a model
model = GenerativeModel("gemini-1.5-flash")

# Patch with instructor
client = instructor.from_vertexai(model)

# Extract data
user = client.generate_content(
    response_model=User,
    contents="Extract the user info: John is 25 years old."
)

import instructor
from openai import OpenAI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Create OpenAI client with Perplexity base URL
client = instructor.from_perplexity(
    OpenAI(base_url="https://api.perplexity.ai", api_key="YOUR_API_KEY")
)

# Extract data
user = client.chat.completions.create(
    model="sonar",  # or other Perplexity models
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

import instructor
from openai import OpenAI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Create OpenAI client with Fireworks base URL
client = instructor.from_fireworks(
    OpenAI(base_url="https://api.fireworks.ai/inference/v1", api_key="YOUR_API_KEY")
)

# Extract data
user = client.chat.completions.create(
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

import instructor
from openai import OpenAI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Create OpenAI client with Anyscale base URL
client = instructor.from_anyscale(
    OpenAI(base_url="https://api.endpoints.anyscale.com/v1", api_key="YOUR_API_KEY")
)

# Extract data
user = client.chat.completions.create(
    model="meta-llama/Llama-3-8b-instruct",
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

import instructor
from openai import OpenAI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Create OpenAI client with Together base URL
client = instructor.from_together(
    OpenAI(base_url="https://api.together.xyz/v1", api_key="YOUR_API_KEY")
)

# Extract data
user = client.chat.completions.create(
    model="togethercomputer/llama-3-8b-instructk",
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

import instructor
from openai import OpenAI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Create OpenAI client with OpenRouter base URL
client = instructor.from_openrouter(
    OpenAI(base_url="https://openrouter.ai/api/v1", api_key="YOUR_API_KEY")
)

# Extract data - access to many models
user = client.chat.completions.create(
    model="google/gemma-7b-instruct", # Or any other model on OpenRouter
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

