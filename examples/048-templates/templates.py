# Prompt Templates 
# Learn to dynamically create prompts using Jinja templating and validate them with Pydantic

# Import the necessary libraries
import openai
import instructor
from pydantic import BaseModel
from typing import List

# Define a simple User model with Pydantic
class User(BaseModel):
    """Extract user information from text."""
    name: str
    age: int

# Patch the OpenAI client with Instructor
client = instructor.from_openai(openai.OpenAI())

# BASIC EXAMPLE: Simple template variable
# Extract data using a template with Jinja variables
# The template variable {{ data }} will be replaced with the value from context
user = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": """Extract the information from the
        following text: `{{ data }}`"""
        }
    ],
    response_model=User,
    context={"data": "John Doe is thirty years old"}
)

# Print the extracted structured data
# Output:
# Name: John Doe
# Age: 30
print(f"Name: {user.name}")
print(f"Age: {user.age}")

# ADVANCED EXAMPLE: Using loops in templates
# Define a model for citations with source references
class Citation(BaseModel):
    source_id: int
    text: str

class Answer(BaseModel):
    """Extract answer with supporting citations"""
    answer: str
    citations: List[Citation]

# Extract data using a template with Jinja loops
advanced_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": """
            You are a {{ role }} answering the following question:
            
            <question>
            {{ question }}
            </question>
            
            Use the following sources to answer the question:
            
            <sources>
            {% for source in sources %}
            <source id="{{ source.id }}">
            {{ source.content }}
            </source>
            {% endfor %}
            </sources>
            
            Provide a concise answer with citations to the relevant sources.
            """
        }
    ],
    response_model=Answer,
    context={
        "role": "research assistant",
        "question": "What are the capitals of France and Japan?",
        "sources": [
            {"id": 1, "content": "Paris is the capital city of France."},
            {"id": 2, "content": "France is located in Western Europe."},
            {"id": 3, "content": "Tokyo is the capital city of Japan."},
            {"id": 4, "content": "Japan is an island country in East Asia."}
        ]
    }
)

# Print the advanced example results
for citation in advanced_response.citations:
    print(f"  Source {citation.source_id}: {citation.text}")
    # Source 1: Paris is the capital city of France.
    # Source 2: France is located in Western Europe.
    # Source 3: Tokyo is the capital city of Japan.
    # Source 4: Japan is an island country in East Asia.

