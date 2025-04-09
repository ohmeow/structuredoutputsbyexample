# Gemini Integration

# Use Instructor with Google's Gemini models for structured data extraction.
# 
# 
# 
# 
# 
# pip install instructor google-generativeai jsonref
# 
import instructor
import google.generativeai as genai
from pydantic import BaseModel

# Configure API key
genai.configure(api_key="YOUR_API_KEY")

class User(BaseModel):
    name: str
    age: int

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

user = client.generate_content(
    response_model=User,
    contents="Extract: John is 25 years old.",
    generation_config={
        "system_instruction": "You are an expert at extracting structured data."
    }
)

user = client.generate_content(
    response_model=User,
    contents=[
        {"role": "user", "parts": ["Extract: John is 25 years old."]}
    ]
)

json_client = instructor.from_gemini(
    genai.GenerativeModel("gemini-1.5-flash"),
    mode=instructor.Mode.GEMINI_JSON
)

user = json_client.generate_content(
    response_model=User,
    contents="Extract: John is 25 years old."
)

import google.auth
import google.auth.transport.requests
import instructor
from openai import OpenAI

# Get Google auth credentials
creds, project = google.auth.default()
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

# Configure Vertex AI endpoint
PROJECT = 'your-project-id'
LOCATION = 'us-central1'  # or your preferred region
endpoint = f'https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/{LOCATION}/endpoints/openapi'

# Create patched OpenAI client pointing to Vertex AI
client = instructor.from_openai(
    OpenAI(base_url=endpoint, api_key=creds.token),
    mode=instructor.Mode.JSON  # JSON mode required
)

# Use OpenAI-style interface
user = client.chat.completions.create(
    model="google/gemini-1.5-flash",
    response_model=User,
    messages=[
        {"role": "user", "content": "Extract: John is 25 years old."}
    ]
)

