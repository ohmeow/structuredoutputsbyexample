# Installing Instructor

# Install the base package
$ pip install instructor

# OpenAI (included by default)
$ pip install instructor
$ export OPENAI_API_KEY=your_openai_key

# Anthropic
$ pip install "instructor[anthropic]"
$ export ANTHROPIC_API_KEY=your_anthropic_key

# Google/Gemini
$ pip install "instructor[google-generativeai]"
export GOOGLE_API_KEY=your_google_key

# Cohere
$ pip install "instructor[cohere]"
$ export COHERE_API_KEY=your_cohere_key

# Mistral
$ pip install "instructor[mistralai]"
$ export MISTRAL_API_KEY=your_mistral_key

# Multiple providers via LiteLLM
$ pip install "instructor[litellm]"