# Gemini Integration

# Use Instructor with Google's Gemini models for structured data extraction.
#
# <b>pip install "instructor[google-genai]"</b>
import instructor
from google import genai
from pydantic import BaseModel


# <b>Initialize and patch the client</b>
# <i>(with gemini api key)</i>
API_KEY = "YOUR_API_KEY"
client = genai.Client(api_key=API_KEY)
client = instructor.from_genai(client, mode=instructor.Mode.GENAI_TOOLS)

# <b>Initialize and patch the client</b>
# <i>(with vertex)</i>
client = genai.Client(vertexai=True, project="your-project-id", location="us-central1")
client = instructor.from_genai(client, mode=instructor.Mode.GENAI_TOOLS)


# <b>Basic usage</b>
#
# Model suggestions:
# - gemini-2.0-flash-lite (fastest)
# - gemini-2.0-flash (faster)
# - gemini-2.5-pro-preview-03-25 (best)
class User(BaseModel):
    name: str
    age: int


response = client.chat.completions.create(
    model="gemini-2.0-flash-001",
    messages=[{"role": "user", "content": "Extract: Jason is 25 years old"}],
    response_model=User,
)
print(response)  # User(name='Jason', age=25)
print(f"Name: {response.name}, Age: {response.age}")  # Name: Jason , Age: 25


# <b>Ensure property ordering</b>
# By default, the API orders properties alphabetically which may be a problem if, for "example", you want to include an `examples` attribute and ensure it appears first.
# #
# In that case, you can add a `Config` class with a `propertyOrdering` attribute and explicitly list the properties in the order they should appear.
class User(BaseModel):
    name: str
    age: int

    class Config:
        propertyOrdering = ["name", "age"]


response = client.chat.completions.create(
    model="gemini-2.0-flash-001",
    messages=[{"role": "user", "content": "Extract: Jason is 25 years old"}],
    response_model=User,
)
print(response)  # User(name='Jason', age=25)
print(f"Name: {response.name}, Age: {response.age}")  # Name: Jason, Age: 25


# <b>Including a system instruction</b>
#
# Use either the `system` parameter or add a system message
response = client.chat.completions.create(
    model="gemini-2.0-flash-001",
    # system="Make everyone 10 years younger you find!",
    messages=[
        {
            "role": "system",
            "content": "Make everyone 10 years younger you find!",
        },
        {
            "role": "user",
            "content": "Extract: Jason is 25 years old",
        },
    ],
    response_model=User,
)
print(response)  # User(name='Jason', age=15)
print(f"Name: {response.name}, Age: {response.age}")  # Name: Jason, Age: 15

# <b></b>

# # Gemini 1.5 Flash (faster)
# flash_model = genai.GenerativeModel("gemini-1.5-flash")
# flash_client = instructor.from_gemini(flash_model, mode=instructor.Mode.GEMINI_TOOLS)

# # Gemini 1.5 Pro (more capable)
# pro_model = genai.GenerativeModel("gemini-1.5-pro")
# pro_client = instructor.from_gemini(pro_model, mode=instructor.Mode.GEMINI_TOOLS)

# user = client.generate_content(
#     response_model=User,
#     contents="Extract: John is 25 years old.",
#     generation_config={
#         "system_instruction": "You are an expert at extracting structured data."
#     },
# )

# user = client.generate_content(
#     response_model=User,
#     contents=[{"role": "user", "parts": ["Extract: John is 25 years old."]}],
# )

# json_client = instructor.from_gemini(
#     genai.GenerativeModel("gemini-1.5-flash"), mode=instructor.Mode.GEMINI_JSON
# )

# user = json_client.generate_content(
#     response_model=User, contents="Extract: John is 25 years old."
# )

# import google.auth
# import google.auth.transport.requests
# import instructor
# from openai import OpenAI

# # Get Google auth credentials
# creds, project = google.auth.default()
# auth_req = google.auth.transport.requests.Request()
# creds.refresh(auth_req)

# # Configure Vertex AI endpoint
# PROJECT = "your-project-id"
# LOCATION = "us-central1"  # or your preferred region
# endpoint = f"https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT}/locations/{LOCATION}/endpoints/openapi"

# # Create patched OpenAI client pointing to Vertex AI
# client = instructor.from_openai(
#     OpenAI(base_url=endpoint, api_key=creds.token),
#     mode=instructor.Mode.JSON,  # JSON mode required
# )

# # Use OpenAI-style interface
# user = client.chat.completions.create(
#     model="google/gemini-1.5-flash",
#     response_model=User,
#     messages=[{"role": "user", "content": "Extract: John is 25 years old."}],
# )
