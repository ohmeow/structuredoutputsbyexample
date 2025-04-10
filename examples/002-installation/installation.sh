# Installing Instructor
# A comprehensive guide to setting up Instructor in your Python environment. This guide covers installation, configuration, and best practices for working with different LLM providers.
# Setting up your development environment correctly is crucial for working with Instructor effectively.
# This guide will help you configure API keys securely and ensure your environment is properly set up for structured outputs.

# Instructor works with all major LLM providers. Installation is simple using pip.

# ## Basic Installation
# Install the base package
pip install instructor

# Install with specific provider dependencies:
# For OpenAI (included by default)
pip install instructor

# For Anthropic
pip install "instructor[anthropic]"

# For Google/Gemini
pip install "instructor[google-generativeai]"

# For Cohere
pip install "instructor[cohere]"

# For Mistral
pip install "instructor[mistralai]"

# For multiple providers via LiteLLM
pip install "instructor[litellm]"

# ## Environment Setup
# 
# Set your API keys as environment variables:
# OpenAI
export OPENAI_API_KEY=your_openai_key

# Anthropic
export ANTHROPIC_API_KEY=your_anthropic_key

# Google/Gemini
export GOOGLE_API_KEY=your_google_key

