# Run the example
# # Installing Instructor
# 
# Instructor works with all major LLM providers. Installation is simple using pip.
# 
# ## Basic Installation
$ # Install the base package
$ pip install instructor

# ## Provider-Specific Installation
# 
# Install with specific provider dependencies:
$ # For OpenAI (included by default)
$ pip install instructor
$ 
$ # For Anthropic
$ pip install "instructor[anthropic]"
$ 
$ # For Google/Gemini
$ pip install "instructor[google-generativeai]"
$ 
$ # For Cohere
$ pip install "instructor[cohere]"
$ 
$ # For Mistral
$ pip install "instructor[mistralai]"
$ 
$ # For multiple providers via LiteLLM
$ pip install "instructor[litellm]"

# ## Environment Setup
# 
# Set your API keys as environment variables:
$ # OpenAI
$ export OPENAI_API_KEY=your_openai_key
$ 
$ # Anthropic
$ export ANTHROPIC_API_KEY=your_anthropic_key
$ 
$ # Google/Gemini
$ export GOOGLE_API_KEY=your_google_key

