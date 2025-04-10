# Gemini Integration
# Learn how to use Instructor with Google's Gemini models for structured data extraction. This guide covers model selection, parameters, and alternative integration methods.
# Google's Gemini models offer powerful capabilities for understanding and processing natural language.
# Instructor allows you to extract structured data from Gemini models with type safety and validation.

# Import necessary libraries
import instructor
import google.generativeai as genai
import google.auth
import google.auth.transport.requests
from openai import OpenAI
from pydantic import BaseModel

# Define a simple model for extraction
class User(BaseModel):
    name: str
    age: int

# Configure API key
genai.configure(api_key="YOUR_API_KEY")

# Create Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Patch with instructor (require specific mode)
client = instructor.from_gemini(
    model,
    mode=instructor.Mode.GEMINI_TOOLS  # or GEMINI_JSON
)

# Using generate_content method
user = client.generate_content(
    response_model=User,
    contents="Extract: John is 25 years old."
)

print(f"Name: {user.name}, Age: {user.age}")
# Output: Name: John, Age: 25

# Different model options
# Gemini 1.5 Flash (faster)
flash_model = genai.GenerativeModel("gemini-1.5-flash")
flash_client = instructor.from_gemini(
    flash_model,
    mode=instructor.Mode.GEMINI_TOOLS
)

# Gemini 1.5 Pro (more capable)
pro_model = genai.GenerativeModel("gemini-1.5-pro")
pro_client = instructor.from_gemini(
    pro_model,
    mode=instructor.Mode.GEMINI_TOOLS
)

# Using system instructions
user = client.generate_content(
    response_model=User,
    contents="Extract: John is 25 years old.",
    generation_config={
        "system_instruction": "You are an expert at extracting structured data."
    }
)

# Using chat format
user = client.generate_content(
    response_model=User,
    contents=[
        {"role": "user", "parts": ["Extract: John is 25 years old."]}
    ]
)

# Using JSON mode instead of tools mode
json_client = instructor.from_gemini(
    genai.GenerativeModel("gemini-1.5-flash"),
    mode=instructor.Mode.GEMINI_JSON
)

user = json_client.generate_content(
    response_model=User,
    contents="Extract: John is 25 years old."
)

# Alternative: Using Vertex AI with OpenAI-compatible interface
# Get Google auth credentials
creds, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

# Configure Vertex AI endpoint
PROJECT = 'your-project-id'
LOCATION = 'us-central1'  # or your preferred region
endpoint = f'https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/{LOCATION}/endpoints/openapi'

# Create patched OpenAI client pointing to Vertex AI
vertex_client = instructor.from_openai(
    OpenAI(base_url=endpoint, api_key=creds.token),
    mode=instructor.Mode.JSON  # JSON mode required
)

# Use OpenAI-style interface
user = vertex_client.chat.completions.create(
    model="google/gemini-1.5-flash",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

