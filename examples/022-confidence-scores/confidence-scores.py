# Working with Confidence Scores

# 

# Add confidence metrics to your structured extractions with Instructor.
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

class PredictionWithConfidence(BaseModel):
    prediction: str = Field(description="The predicted answer or category")
    confidence: float = Field(
        gt=0, le=1,  # Greater than 0, less than or equal to 1
        description="Confidence score between 0 and 1 (higher = more confident)"
    )

# Patch the client
client = instructor.from_openai(OpenAI())

def predict_with_confidence(question: str, context: str) -> PredictionWithConfidence:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=PredictionWithConfidence,
        messages=[
            {
                "role": "system",
                "content": "Answer the question based on the provided context. Include a confidence score."
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuestion: {question}"
            }
        ]
    )

# Test with varying levels of confidence
contexts = [
    # High confidence - direct answer in context
    "The Golden Gate Bridge was completed in 1937. It is located in San Francisco, California.",

    # Medium confidence - partial information
    "The Golden Gate Bridge is a famous landmark in California. Many tourists visit it each year.",

    # Low confidence - minimal relevant information
    "California has many famous landmarks and tourist attractions that draw visitors from around the world."
]

question = "When was the Golden Gate Bridge completed?"

for i, context in enumerate(contexts):
    result = predict_with_confidence(question, context)
    print(f"Example {i+1}:")
    print(f"Context: '{context}'")
    print(f"Question: '{question}'")
    print(f"Prediction: {result.prediction}")
    print(f"Confidence: {result.confidence:.2f}\n")

# Example Output:
# Example 1:
# Prediction: 1937
# Confidence: 0.98
#
# Example 2:
# Prediction: The completion date is not specified in the context.
# Confidence: 0.45
#
# Example 3:
# Prediction: The context does not provide information about the Golden Gate Bridge's completion date.
# Confidence: 0.95

from pydantic import BaseModel, Field
from typing import Literal

class ClassificationWithConfidence(BaseModel):
    category: Literal["sports", "politics", "technology", "entertainment", "business"]
    confidence: float = Field(
        gt=0, le=1,
        description="Confidence score between 0 and 1"
    )

    @property
    def is_reliable(self) -> bool:
        return self.confidence >= 0.7  # Threshold for reliability

def classify_with_confidence(text: str) -> ClassificationWithConfidence:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=ClassificationWithConfidence,
        messages=[
            {
                "role": "system",
                "content": "Classify the text into one of these categories: sports, politics, technology, entertainment, business."
            },
            {"role": "user", "content": text}
        ]
    )

# Test with examples
examples = [
    "Apple announced its new M3 chip with significantly improved performance.",  # Clear tech
    "The game went into overtime after a last-minute equalizer.",  # Clear sports
    "The gathering included discussion of market trends and artistic influences."  # Ambiguous
]

for text in examples:
    result = classify_with_confidence(text)
    print(f"Text: '{text}'")
    print(f"Category: {result.category}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reliable: {result.is_reliable}\n")

# Example Output:
# Text: 'Apple announced its new M3 chip with significantly improved performance.'
# Category: technology
# Confidence: 0.95
# Reliable: True
#
# Text: 'The game went into overtime after a last-minute equalizer.'
# Category: sports
# Confidence: 0.91
# Reliable: True
#
# Text: 'The gathering included discussion of market trends and artistic influences.'
# Category: business
# Confidence: 0.51
# Reliable: False

from pydantic import BaseModel, Field
from typing import List

class PredictionOption(BaseModel):
    value: str
    confidence: float = Field(gt=0, le=1)

class MultipleOptions(BaseModel):
    options: List[PredictionOption] = Field(
        description="List of possible answers with confidence scores",
        min_items=1
    )

    @property
    def best_option(self) -> PredictionOption:
        return max(self.options, key=lambda x: x.confidence)

def generate_options(question: str) -> MultipleOptions:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=MultipleOptions,
        messages=[
            {
                "role": "system",
                "content": "Generate 2-4 possible answers to the question with confidence scores."
            },
            {"role": "user", "content": question}
        ]
    )

# Test with an ambiguous question
question = "What year is considered the beginning of the modern internet?"

result = generate_options(question)

print(f"Question: '{question}'")
print("Possible answers:")
for option in sorted(result.options, key=lambda x: x.confidence, reverse=True):
    print(f"- {option.value} (confidence: {option.confidence:.2f})")

print(f"\nBest option: {result.best_option.value} (confidence: {result.best_option.confidence:.2f})")

from pydantic import BaseModel, Field
from typing import Dict, List

class ConfidenceMatrix(BaseModel):
    category_scores: Dict[str, float] = Field(
        description="Confidence scores for each possible category"
    )
    most_likely_category: str = Field(
        description="The category with the highest confidence score"
    )
    reliability: Literal["high", "medium", "low"] = Field(
        description="Reliability assessment of the classification"
    )

def multi_category_confidence(text: str, categories: List[str]) -> ConfidenceMatrix:
    categories_str = ", ".join(categories)
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=ConfidenceMatrix,
        messages=[
            {
                "role": "system",
                "content": f"""Analyze the text and provide confidence scores for each possible category: {categories_str}.
                Confidence scores should be between 0 and 1, sum to 1.0, and represent the probability of the text belonging to each category.
                Also assess if the classification reliability is high (clear winner >0.7), medium (top score 0.4-0.7), or low (ambiguous, top score <0.4)."""
            },
            {"role": "user", "content": text}
        ]
    )

# Test with examples
categories = ["health", "finance", "technology", "travel", "education"]
text = "The new smartwatch can track your heart rate, sleep patterns, and activity levels throughout the day."

result = multi_category_confidence(text, categories)

print(f"Text: '{text}'")
print("\nConfidence Scores:")
for category, score in sorted(result.category_scores.items(), key=lambda x: x[1], reverse=True):
    print(f"- {category}: {score:.2f}")

print(f"\nMost Likely Category: {result.most_likely_category}")
print(f"Reliability: {result.reliability}")

from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal
from enum import Enum

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Extraction(BaseModel):
    value: str
    confidence: float = Field(gt=0, le=1)
    confidence_level: ConfidenceLevel
    requires_human_review: bool

class ExtractionResult(BaseModel):
    extracted_info: Extraction
    alternative_values: Optional[List[str]] = None
    extraction_notes: Optional[str] = None
    suggested_action: Literal["accept", "review", "reject"] = Field(
        description="Recommended action based on confidence: accept (high confidence), review (medium), reject (low)"
    )

def extract_with_decision(text: str, field_to_extract: str) -> ExtractionResult:
    return client.chat.completions.create(
        model="gpt-4",  # Better judgement with GPT-4
        response_model=ExtractionResult,
        messages=[
            {
                "role": "system",
                "content": f"""Extract the {field_to_extract} from the text with a confidence score.
                Assess confidence level (high: >0.8, medium: 0.5-0.8, low: <0.5) and determine if human review is needed.
                Recommend an action (accept/review/reject) based on confidence."""
            },
            {"role": "user", "content": text}
        ]
    )

# Test with varying examples
examples = [
    "Patient's DOB: 04/15/1985. Patient presented with symptoms of...",  # Clear
    "The pt. was born in the mid-1980s (possibly '85) and first presented...",  # Uncertain
    "Patient demographic information will be provided in a follow-up report."  # Missing
]

for text in examples:
    result = extract_with_decision(text, "date of birth")
    print(f"Text: '{text}'")
    print(f"Extracted Value: {result.extracted_info.value}")
    print(f"Confidence: {result.extracted_info.confidence:.2f} ({result.extracted_info.confidence_level})")
    print(f"Requires Human Review: {result.extracted_info.requires_human_review}")
    print(f"Suggested Action: {result.suggested_action}")

    if result.alternative_values:
        print(f"Alternative Values: {', '.join(result.alternative_values)}")
    if result.extraction_notes:
        print(f"Notes: {result.extraction_notes}")
    print()

