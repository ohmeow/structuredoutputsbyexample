# Other Provider Integrations
# Explore additional LLM provider integrations with Instructor beyond the major ones. This guide demonstrates how to use Instructor with various alternative providers.
# The LLM ecosystem is diverse with many providers offering specialized models and capabilities.
# Instructor provides a consistent interface across these providers, making it easy to switch between them or use multiple providers.

# Import necessary libraries
import instructor
from pydantic import BaseModel
from openai import OpenAI
from litellm import completion
from vertexai.preview.generative_models import GenerativeModel

# Define a simple model for extraction - used with all providers
class User(BaseModel):
    name: str
    age: int

# LiteLLM Integration
# Patch LiteLLM completion function to support many providers
litellm_client = instructor.from_litellm(completion)

# Use with any provider supported by LiteLLM
litellm_user = litellm_client.chat.completions.create(
    model="gpt-3.5-turbo",  # or any other provider/model combination
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

# Google Vertex AI Integration (direct)
# Create a model
vertex_model = GenerativeModel("gemini-1.5-flash")

# Patch with instructor
vertex_client = instructor.from_vertexai(vertex_model)

# Extract data
vertex_user = vertex_client.generate_content(
    response_model=User,
    contents="Extract the user info: John is 25 years old."
)

# Perplexity AI Integration
# Create OpenAI client with Perplexity base URL
perplexity_client = instructor.from_perplexity(
    OpenAI(base_url="https://api.perplexity.ai", api_key="YOUR_API_KEY")
)

# Extract data
perplexity_user = perplexity_client.chat.completions.create(
    model="sonar",  # or other Perplexity models
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

# Fireworks AI Integration
# Create OpenAI client with Fireworks base URL
fireworks_client = instructor.from_fireworks(
    OpenAI(base_url="https://api.fireworks.ai/inference/v1", api_key="YOUR_API_KEY")
)

# Extract data
fireworks_user = fireworks_client.chat.completions.create(
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

# Anyscale Integration
# Create OpenAI client with Anyscale base URL
anyscale_client = instructor.from_anyscale(
    OpenAI(base_url="https://api.endpoints.anyscale.com/v1", api_key="YOUR_API_KEY")
)

# Extract data
anyscale_user = anyscale_client.chat.completions.create(
    model="meta-llama/Llama-3-8b-instruct",
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

# Together AI Integration
# Create OpenAI client with Together base URL
together_client = instructor.from_together(
    OpenAI(base_url="https://api.together.xyz/v1", api_key="YOUR_API_KEY")
)

# Extract data
together_user = together_client.chat.completions.create(
    model="togethercomputer/llama-3-8b-instructk",
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

# OpenRouter Integration
# Create OpenAI client with OpenRouter base URL
openrouter_client = instructor.from_openrouter(
    OpenAI(base_url="https://openrouter.ai/api/v1", api_key="YOUR_API_KEY")
)

# Extract data - access to many models
openrouter_user = openrouter_client.chat.completions.create(
    model="google/gemma-7b-instruct", # Or any other model on OpenRouter
    response_model=User,
    messages=[
        {"role": "user", "content": "John is 25 years old."}
    ]
)

