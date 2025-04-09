# Sentiment Analysis

# 

# Perform sentiment analysis on text with structured outputs using Instructor.
from pydantic import BaseModel, Field
from typing import Literal
import instructor
from openai import OpenAI

class Sentiment(BaseModel):
    """Sentiment analysis result"""

    sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="The overall sentiment of the text"
    )

# Patch the client
client = instructor.from_openai(OpenAI())

def analyze_sentiment(text: str) -> Sentiment:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Sentiment,
        messages=[
            {"role": "system", "content": "Analyze the sentiment of the provided text."},
            {"role": "user", "content": f"Text: {text}"}
        ]
    )

# Test with examples
examples = [
    "I absolutely love this product! It exceeded all my expectations.",
    "The service was okay. Nothing special but got the job done.",
    "This is the worst experience I've ever had. Complete waste of money."
]

for text in examples:
    result = analyze_sentiment(text)
    print(f"Text: '{text}'")
    print(f"Sentiment: {result.sentiment}\n")

# Example Output:
# Text: 'I absolutely love this product! It exceeded all my expectations.'
# Sentiment: positive
#
# Text: 'The service was okay. Nothing special but got the job done.'
# Sentiment: neutral
#
# Text: 'This is the worst experience I've ever had. Complete waste of money.'
# Sentiment: negative

from pydantic import BaseModel, Field

class SentimentWithScore(BaseModel):
    """Sentiment analysis with numeric score"""

    score: float = Field(
        ge=-1.0, le=1.0,  # Between -1.0 and 1.0
        description="Sentiment score from -1.0 (very negative) to 1.0 (very positive)"
    )

    @property
    def sentiment(self) -> str:
        if self.score > 0.3:
            return "positive"
        elif self.score < -0.3:
            return "negative"
        else:
            return "neutral"

def analyze_sentiment_with_score(text: str) -> SentimentWithScore:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=SentimentWithScore,
        messages=[
            {
                "role": "system",
                "content": "Analyze the sentiment of the text and provide a score from -1.0 (very negative) to 1.0 (very positive)."
            },
            {"role": "user", "content": f"Text: {text}"}
        ]
    )

# Test with examples
examples = [
    "The movie was absolutely phenomenal. Best I've seen in years!",
    "The new update is slightly better than the previous version.",
    "I'm really disappointed with the customer service response time."
]

for text in examples:
    result = analyze_sentiment_with_score(text)
    print(f"Text: '{text}'")
    print(f"Score: {result.score:.2f}")
    print(f"Sentiment: {result.sentiment}\n")

# Example Output:
# Text: 'The movie was absolutely phenomenal. Best I've seen in years!'
# Score: 0.95
# Sentiment: positive
#
# Text: 'The new update is slightly better than the previous version.'
# Score: 0.20
# Sentiment: neutral
#
# Text: 'I'm really disappointed with the customer service response time.'
# Score: -0.75
# Sentiment: negative

from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class AspectSentiment(BaseModel):
    aspect: str = Field(description="The specific aspect being evaluated")
    sentiment: Literal["positive", "neutral", "negative"]
    explanation: str = Field(description="Brief explanation of the sentiment")

class DetailedSentiment(BaseModel):
    overall_sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="The overall sentiment of the entire text"
    )
    aspects: List[AspectSentiment] = Field(
        description="Sentiment breakdown by specific aspects mentioned in the text"
    )
    summary: str = Field(
        description="A brief summary of the sentiment analysis"
    )

def analyze_detailed_sentiment(text: str) -> DetailedSentiment:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=DetailedSentiment,
        messages=[
            {
                "role": "system",
                "content": "Perform a detailed sentiment analysis, breaking down sentiment by aspects."
            },
            {"role": "user", "content": f"Text: {text}"}
        ]
    )

# Test with a product review
review = """
    I recently purchased the XYZ Bluetooth headphones. The sound quality is amazing and
    battery life exceeds expectations - nearly 30 hours on a single charge! However,
    they're a bit too tight on my head after a few hours, which gets uncomfortable.
    The price was reasonable for the quality. Customer service was unhelpful when I asked
    about adjustment options.
"""

result = analyze_detailed_sentiment(review)

print(f"Overall Sentiment: {result.overall_sentiment}")
print("\nAspect Breakdown:")
for aspect in result.aspects:
    print(f"- {aspect.aspect}: {aspect.sentiment}")
    print(f"  {aspect.explanation}")

print(f"\nSummary: {result.summary}")

# Example Output:
# Overall Sentiment: positive
#
# Aspect Breakdown:
# - Sound Quality: positive
#   The reviewer describes the sound quality as "amazing"
# - Battery Life: positive
#   The battery life "exceeds expectations" with nearly 30 hours on a single charge
# - Comfort: negative
#   The headphones are described as "too tight" and "uncomfortable" after extended use
# - Price: positive
#   The reviewer found the price "reasonable for the quality"
# - Customer Service: negative
#   Customer service was described as "unhelpful"
#
# Summary: The review is overall positive, particularly praising sound quality, battery life, and price,
# but notes issues with comfort and customer service.

from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime

class Emotion(BaseModel):
    name: str
    intensity: float = Field(ge=0, le=1)  # 0-1 scale

class SocialMediaSentiment(BaseModel):
    primary_sentiment: Literal["positive", "neutral", "negative"]
    emotions: List[Emotion] = Field(description="Emotions detected in the text with intensity")
    is_sarcastic: bool = Field(description="Whether the text appears to contain sarcasm")
    topics: List[str] = Field(description="Key topics mentioned in the text")
    action_items: Optional[List[str]] = Field(
        default=None,
        description="Suggested actions if this is a customer complaint or request"
    )
    urgency: int = Field(
        ge=1, le=5,
        description="Urgency level from 1 (not urgent) to 5 (extremely urgent)"
    )

def analyze_social_post(text: str) -> SocialMediaSentiment:
    return client.chat.completions.create(
        model="gpt-4",  # Using GPT-4 for more nuanced analysis
        response_model=SocialMediaSentiment,
        messages=[
            {
                "role": "system",
                "content": "Analyze this social media post for sentiment, emotions, sarcasm, and topics."
            },
            {"role": "user", "content": f"Social Media Post: {text}"}
        ]
    )

# Example social media posts
posts = [
    "@AirlineX Your customer service is just AMAZING! 3 hours on hold and then hung up on. Can't wait to fly with you again... #sarcasm #badservice",
    "Just tried the new coffee shop downtown and WOW! Best latte I've ever had, friendly staff, and great atmosphere. Definitely my new regular spot! #coffee #happy"
]

for post in posts:
    result = analyze_social_post(post)
    print(f"\nPost: '{post}'")
    print(f"Primary Sentiment: {result.primary_sentiment}")
    print(f"Sarcastic: {result.is_sarcastic}")

    print("\nEmotions:")
    for emotion in result.emotions:
        print(f"- {emotion.name}: {emotion.intensity:.2f}")

    print(f"\nTopics: {', '.join(result.topics)}")
    print(f"Urgency: {result.urgency}/5")

    if result.action_items:
        print("\nSuggested Actions:")
        for item in result.action_items:
            print(f"- {item}")

