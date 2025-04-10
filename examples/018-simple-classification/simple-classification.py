# Simple Classification
# Perform single-label classification with Instructor and structured outputs.

# Import the necessary libraries
from pydantic import BaseModel, Field
from typing import Literal
import instructor
from openai import OpenAI

# Define a Classification model with Pydantic
class Classification(BaseModel):
    """A single-label classification for text as SPAM or NOT_SPAM"""

    label: Literal["SPAM", "NOT_SPAM"] = Field(
        description="The classification label, either SPAM or NOT_SPAM"
    )

# Patch the client
client = instructor.from_openai(OpenAI())

# Define a function to classify text
def classify_text(text: str) -> Classification:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Classification,
        messages=[
            {
                "role": "system",
                "content": """
                You are an email spam classifier. Classify the provided text as either SPAM or NOT_SPAM.

                Examples of SPAM:
                - "Claim your free prize now!"
                - "Make $1000 a day working from home"
                - "Limited time offer - 90% discount"

                Examples of NOT_SPAM:
                - "Can we schedule a meeting tomorrow?"
                - "Here's the report you requested"
                - "Please review the attached document"
                """
            },
            {"role": "user", "content": f"Classify this text: {text}"}
        ]
    )

# Test with examples
spam_text = "URGENT: Your account has been compromised. Click here to verify details!"
legit_text = "Please review the meeting notes and provide your feedback by Friday."

# Output:
# Legit classification: NOT_SPAM
spam_result = classify_text("URGENT: Your account has been compromised. Click here to verify details!")

# Output:
# Legit classification: NOT_SPAM
legit_result = classify_text("Please review the meeting notes and provide your feedback by Friday.")
