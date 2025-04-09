# Multi-label Classification

# Extract multiple labels from text using Instructor.
from pydantic import BaseModel, Field
from typing import List
import instructor
from openai import OpenAI

class MultiLabelClassification(BaseModel):
    """Multi-label classification of text content"""

    labels: List[str] = Field(
        description="List of applicable category labels for the text"
    )

# Patch the client
client = instructor.from_openai(OpenAI())

def classify_text(text: str) -> MultiLabelClassification:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=MultiLabelClassification,
        messages=[
            {
                "role": "system",
                "content": """
                Classify the text into one or more of these categories:
                - Technology
                - Finance
                - Health
                - Sports
                - Entertainment
                - Politics
                - Science
                - Education

                Return all categories that apply to the text.
                """
            },
            {"role": "user", "content": f"Text for classification: {text}"}
        ]
    )

# Test with an example
article = """
    Bitcoin prices surged to a new all-time high today as several tech companies announced
    plans to add the cryptocurrency to their balance sheets. Health officials warned that
    the excitement might cause stress for some investors.
"""

result = classify_text(article)

print(f"Text: '{article}'")
print(f"Labels: {', '.join(result.labels)}")
# Example Output: Labels: Technology, Finance, Health

from enum import Enum
from pydantic import BaseModel, Field
from typing import List

# Define fixed categories as an enum
class Category(str, Enum):
    BUSINESS = "business"
    TECHNOLOGY = "technology"
    POLITICS = "politics"
    HEALTH = "health"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"
    SCIENCE = "science"
    EDUCATION = "education"

class EnumMultiLabelClassification(BaseModel):
    """Multi-label classification using predefined categories"""

    categories: List[Category] = Field(
        description="List of applicable categories from the predefined set"
    )

def classify_with_enums(text: str) -> EnumMultiLabelClassification:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=EnumMultiLabelClassification,
        messages=[
            {"role": "system", "content": "Classify the text into one or more predefined categories."},
            {"role": "user", "content": f"Text for classification: {text}"}
        ]
    )

article = """
    New educational technology is transforming classrooms across the country.
    Students are using AI-powered tools to enhance their learning experiences.
"""

result = classify_with_enums(article)

print(f"Text: '{article}'")
print(f"Categories: {', '.join([c.value for c in result.categories])}")
# Example Output: Categories: technology, education

from pydantic import BaseModel, Field
from typing import List, Dict

class LabelWithConfidence(BaseModel):
    label: str
    confidence: float = Field(gt=0, le=1)  # Between 0 and 1

class ConfidenceClassification(BaseModel):
    labels: List[LabelWithConfidence] = Field(
        description="List of applicable labels with confidence scores"
    )

def classify_with_confidence(text: str) -> ConfidenceClassification:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=ConfidenceClassification,
        messages=[
            {
                "role": "system",
                "content": """
                Classify the text into these categories and provide confidence scores (0-1):
                - Technology
                - Finance
                - Health
                - Sports
                - Entertainment
                Only include categories that apply with a confidence score over 0.4.
                """
            },
            {"role": "user", "content": f"Text for classification: {text}"}
        ]
    )

article = """
    The new smartphone features a built-in heart rate monitor that can alert users
    about potential cardiac issues while they exercise.
"""

result = classify_with_confidence(article)

print(f"Text: '{article}'")
print("Labels with confidence:")
for label in result.labels:
    print(f"- {label.label}: {label.confidence:.2f}")

# Example Output:
# Labels with confidence:
# - Technology: 0.95
# - Health: 0.85
# - Sports: 0.62

from pydantic import BaseModel, Field
from typing import List, Optional

class SubCategory(BaseModel):
    name: str
    confidence: float = Field(gt=0, le=1)

class MainCategory(BaseModel):
    name: str
    confidence: float = Field(gt=0, le=1)
    subcategories: List[SubCategory] = []

class HierarchicalClassification(BaseModel):
    categories: List[MainCategory] = Field(
        description="Hierarchical categories with confidence scores"
    )

def classify_hierarchical(text: str) -> HierarchicalClassification:
    return client.chat.completions.create(
        model="gpt-4",  # More complex tasks work better with GPT-4
        response_model=HierarchicalClassification,
        messages=[
            {
                "role": "system",
                "content": """
                Classify the text into main categories and subcategories:

                Main categories:
                - Technology (subcategories: Hardware, Software, AI, Internet)
                - Science (subcategories: Physics, Biology, Chemistry, Astronomy)
                - Health (subcategories: Fitness, Nutrition, Medical, Mental Health)

                Return only relevant categories with confidence scores.
                """
            },
            {"role": "user", "content": f"Text for classification: {text}"}
        ]
    )

article = """
    Researchers have developed a new AI algorithm that can detect early signs of
    Alzheimer's disease from brain scans with 94% accuracy. The deep learning software
    could help doctors diagnose patients years earlier than current methods.
"""

result = classify_hierarchical(article)

print(f"Text: '{article}'")
print("Classification:")
for category in result.categories:
    print(f"- {category.name} ({category.confidence:.2f})")
    for subcategory in category.subcategories:
        print(f"  - {subcategory.name} ({subcategory.confidence:.2f})")

# Example Output:
# Classification:
# - Technology (0.90)
#   - AI (0.95)
#   - Software (0.80)
# - Health (0.85)
#   - Medical (0.90)
# - Science (0.75)
#   - Biology (0.70)

