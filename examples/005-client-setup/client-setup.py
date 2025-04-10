# Client Setup
# Configure Instructor clients for different LLM providers. Learn about extraction modes and client configuration options.
# Working with multiple LLM providers requires understanding their specific integration patterns.
# Instructor provides a unified interface across providers while respecting their unique capabilities.

# Import necessary libraries
import instructor
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
import cohere
from mistralai.client import MistralClient
from instructor import Mode

# OpenAI setup
# Default mode for OpenAI is TOOLS (function calling)
openai_client = instructor.from_openai(OpenAI())

# You can also specify a different mode
openai_json_client = instructor.from_openai(
    OpenAI(),
    mode=instructor.Mode.JSON  # Use JSON mode instead
)

# Anthropic setup
# Default mode is TOOLS for Claude 3
anthropic_client = instructor.from_anthropic(Anthropic())

# Use JSON mode if needed
anthropic_json_client = instructor.from_anthropic(
    Anthropic(),
    mode=instructor.Mode.JSON
)

# Google Gemini setup
# Configure Gemini
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Gemini needs a specific mode
gemini_client = instructor.from_gemini(
    model,
    mode=instructor.Mode.GEMINI_TOOLS  # or GEMINI_JSON
)

# Cohere setup
# Create Cohere client
cohere_client = cohere.Client("YOUR_API_KEY")

# Patch with instructor
cohere_instructor_client = instructor.from_cohere(cohere_client)

# Mistral setup
mistral_client = MistralClient(api_key="YOUR_API_KEY")

# Patch with instructor
mistral_instructor_client = instructor.from_mistral(mistral_client)

# Available modes overview
# Mode.TOOLS         # OpenAI function calling format (default for OpenAI)
# Mode.JSON          # Plain JSON generation
# Mode.MD_JSON       # Markdown JSON (used by some providers)
# Mode.ANTHROPIC_TOOLS # Claude tools mode (default for Anthropic)
# Mode.GEMINI_TOOLS  # Gemini tools format
# Mode.GEMINI_JSON   # Gemini JSON format

