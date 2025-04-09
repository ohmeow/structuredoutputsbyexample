# Client Setup

# Configure Instructor clients for different LLM providers. Learn about extraction modes and client configuration options.

# Set up Instructor with different LLM providers. Each provider requires slightly different setup.
import instructor
from openai import OpenAI

# Default mode for OpenAI is TOOLS (function calling)
client = instructor.from_openai(OpenAI())

# You can also specify a different mode
client = instructor.from_openai(
    OpenAI(),
    mode=instructor.Mode.JSON  # Use JSON mode instead
)

import instructor
from anthropic import Anthropic

# Default mode is TOOLS for Claude 3
client = instructor.from_anthropic(Anthropic())

# Use JSON mode if needed
client = instructor.from_anthropic(
    Anthropic(),
    mode=instructor.Mode.JSON
)

import instructor
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Gemini needs a specific mode
client = instructor.from_gemini(
    model,
    mode=instructor.Mode.GEMINI_TOOLS  # or GEMINI_JSON
)

import instructor
import cohere

# Create Cohere client
cohere_client = cohere.Client("YOUR_API_KEY")

# Patch with instructor
client = instructor.from_cohere(cohere_client)

import instructor
from mistralai.client import MistralClient

mistral_client = MistralClient(api_key="YOUR_API_KEY")

# Patch with instructor
client = instructor.from_mistral(mistral_client)

# Instructor supports different modes for different providers:
from instructor import Mode

# Available modes
Mode.TOOLS         # OpenAI function calling format (default for OpenAI)
Mode.JSON          # Plain JSON generation
Mode.MD_JSON       # Markdown JSON (used by some providers)
Mode.ANTHROPIC_TOOLS # Claude tools mode (default for Anthropic)
Mode.GEMINI_TOOLS  # Gemini tools format
Mode.GEMINI_JSON   # Gemini JSON format

