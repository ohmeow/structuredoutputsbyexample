# Multi-label Classification Example
#
# This example demonstrates various approaches to multi-label classification using Instructor:
# 1. Basic multi-label classification with string labels
# 2. Using Enums for predefined categories
# 3. Classification with confidence scores
# 4. Hierarchical classification with main and subcategories
#
# Each approach shows how to structure your Pydantic models for different classification needs.


# Import the necessary libraries
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import instructor
from openai import OpenAI

# Initialize the instructor-enhanced OpenAI client
client = instructor.from_openai(OpenAI())

# Define a MultiLabelClassification model with Pydantic
class MultiLabelClassification(BaseModel):
    """Multi-label classification of text content"""
    labels: List[str] = Field(
        description="List of applicable category labels for the text"
    )

# Define a function to classify text
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

# Define a Category enum for predefined categories
class Category(str, Enum):
    BUSINESS = "business"
    TECHNOLOGY = "technology"
    POLITICS = "politics"
    HEALTH = "health"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"
    SCIENCE = "science"
    EDUCATION = "education"

# Define a function to classify text with enums
class EnumMultiLabelClassification(BaseModel):
    """Multi-label classification using predefined categories"""
    categories: List[Category] = Field(
        description="List of applicable categories from the predefined set"
    )

# Define a function to classify text with enums
def classify_with_enums(text: str) -> EnumMultiLabelClassification:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=EnumMultiLabelClassification,
        messages=[
            {"role": "system", "content": "Classify the text into one or more predefined categories."},
            {"role": "user", "content": f"Text for classification: {text}"}
        ]
    )

# Define a function to classify text with confidence scores
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

# Define a function to classify text hierarchically
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

# Define a function to classify text hierarchically
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

# Test the multi-label classification
# Output:
# Labels: technology, science, health
result = classify_text("Researchers have developed a new AI algorithm that can detect early signs of Alzheimer's disease from brain scans with 94% accuracy. The deep learning software could help doctors diagnose patients years earlier than current methods.")
