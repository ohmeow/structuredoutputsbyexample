# Simple Classification

# Perform single-label classification with Instructor and structured outputs.
from pydantic import BaseModel, Field
from typing import Literal
import instructor
from openai import OpenAI

class Classification(BaseModel):
    """A single-label classification for text as SPAM or NOT_SPAM"""

    label: Literal["SPAM", "NOT_SPAM"] = Field(
        description="The classification label, either SPAM or NOT_SPAM"
    )

# Patch the client
client = instructor.from_openai(OpenAI())

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

spam_result = classify_text(spam_text)
legit_result = classify_text(legit_text)

print(f"Text: '{spam_text}'")
print(f"Classification: {spam_result.label}")
# Output: Classification: SPAM

print(f"\nText: '{legit_text}'")
print(f"Classification: {legit_result.label}")
# Output: Classification: NOT_SPAM

from pydantic import BaseModel, Field
from typing import Literal

class ClassificationWithConfidence(BaseModel):
    label: Literal["SPAM", "NOT_SPAM"]
    confidence: float = Field(
        gt=0, le=1,  # Greater than 0, less than or equal to 1
        description="Confidence score between 0 and 1 (higher = more confident)"
    )

def classify_with_confidence(text: str) -> ClassificationWithConfidence:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=ClassificationWithConfidence,
        messages=[
            {
                "role": "system",
                "content": "Classify the text as SPAM or NOT_SPAM with a confidence score."
            },
            {"role": "user", "content": f"Classify this text: {text}"}
        ]
    )

borderline_text = "Get your free account upgrade today. Limited availability."
result = classify_with_confidence(borderline_text)

print(f"Text: '{borderline_text}'")
print(f"Classification: {result.label}")
print(f"Confidence: {result.confidence:.2f}")
# Example Output:
# Classification: SPAM
# Confidence: 0.75

from pydantic import BaseModel, Field
from typing import Literal

class DetailedClassification(BaseModel):
    label: Literal["SPAM", "NOT_SPAM"]
    explanation: str = Field(
        description="Detailed reasoning for this classification"
    )
    spam_indicators: list[str] = Field(
        default_factory=list,
        description="List of specific elements that indicate spam, if any"
    )

def classify_with_details(text: str) -> DetailedClassification:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=DetailedClassification,
        messages=[
            {"role": "system", "content": "Classify the text and provide a detailed explanation."},
            {"role": "user", "content": f"Classify this text: {text}"}
        ]
    )

text = "CONGRATULATIONS! You've been selected to receive a free iPhone! Click now to claim: bit.ly/claim-prize"
result = classify_with_details(text)

print(f"Text: '{text}'")
print(f"Classification: {result.label}")
print(f"Explanation: {result.explanation}")
print("Spam indicators:")
for indicator in result.spam_indicators:
    print(f"- {indicator}")

from typing import List

def classify_batch(texts: List[str]) -> List[Classification]:
    # Use a batch prompt to classify multiple texts at once
    formatted_texts = "\n\n".join([f"Text {i+1}: {text}" for i, text in enumerate(texts)])

    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=List[Classification],
        messages=[
            {"role": "system", "content": "Classify each text as SPAM or NOT_SPAM."},
            {"role": "user", "content": f"Classify these texts:\n\n{formatted_texts}"}
        ]
    )

# Test with a batch of texts
texts = [
    "Your application has been approved. Sign the documents at your earliest convenience.",
    "WINNER! You've been selected to receive $1000! Send your bank details now!",
    "Meeting rescheduled to 3PM tomorrow. Same Zoom link."
]

results = classify_batch(texts)

for i, (text, result) in enumerate(zip(texts, results)):
    print(f"Text {i+1}: '{text}'")
    print(f"Classification: {result.label}\n")

# Output:# Text 1: 'Your application has been approved. Sign the documents at your earliest convenience.'# Classification: NOT_SPAM## Text 2: 'WINNER! You've been selected to receive $1000! Send your bank details now!'# Classification: SPAM## Text 3: 'Meeting rescheduled to 3PM tomorrow. Same Zoom link.'# Classification: NOT_SPAM

