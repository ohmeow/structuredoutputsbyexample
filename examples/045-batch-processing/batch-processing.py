# Batch Processing

# Implement batch processing for efficient data extraction. Instructor provides structured output for easier data analysis of large datasets.

# Instructor supports batch processing for efficiently handling multiple requests, which is essential for large-scale data processing.
import asyncio
import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from typing import List, Tuple

# Initialize the async client with instructor
client = instructor.from_openai(AsyncOpenAI())

# Semaphore to limit concurrent requests (respect API rate limits)
sem = asyncio.Semaphore(5)

# Define a model for sentiment analysis
class SentimentAnalysis(BaseModel):
    sentiment: str = Field(description="The sentiment of the text (positive, negative, or neutral)")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0")
    reasoning: str = Field(description="Brief explanation for the sentiment classification")

# Function to analyze sentiment of a single text
async def analyze_sentiment(text: str) -> Tuple[str, SentimentAnalysis]:
    async with sem:  # Rate limiting
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_model=SentimentAnalysis,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this text: {text}"
                }
            ]
        )
        return text, result

# Process a batch of texts efficiently with parallel processing
async def process_batch(texts: List[str]):
    tasks = [analyze_sentiment(text) for text in texts]  # Create tasks for all texts

    # Collect results as tasks complete (in any order)
    results = []
    for task in asyncio.as_completed(tasks):
        original_text, sentiment = await task
        results.append({
            "text": original_text,
            "sentiment": sentiment.sentiment,
            "confidence": sentiment.confidence,
            "reasoning": sentiment.reasoning
        })

    return results

# Example usage
async def main():
    texts = [
        "I absolutely love this product! It's amazing.",
        "The service was terrible and the staff was rude.",
        "The weather is cloudy today with a chance of rain.",
        "I'm disappointed with the quality of this item.",
        "The conference was informative and well-organized."
    ]

    results = await process_batch(texts)

    for result in results:
        print(f"Text: {result['text']}")
        print(f"Sentiment: {result['sentiment']} (Confidence: {result['confidence']:.2f})")
        print(f"Reasoning: {result['reasoning']}")
        print("-" * 50)

# Run the example
if __name__ == "__main__":
    asyncio.run(main())

# For larger datasets, you can implement a more comprehensive batch processing solution:
import json
import asyncio
import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Dict, Any, Optional

# Initialize the client
client = instructor.from_openai(AsyncOpenAI())

# Define classification types
class Category(str, Enum):
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    FEATURE = "FEATURE"
    SUPPORT = "SUPPORT"
    OTHER = "OTHER"

class FeedbackClassification(BaseModel):
    categories: List[Category] = Field(description="Categories that apply to this feedback")
    priority: int = Field(description="Priority score from 1-5, where 5 is highest priority", ge=1, le=5)
    analysis: str = Field(description="Brief analysis of the feedback")

# Process function with error handling and retries
async def process_item(item: str, retry_count: int = 2) -> Dict[str, Any]:
    attempts = 0
    while attempts <= retry_count:
        try:
            result = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_model=FeedbackClassification,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a customer feedback analyzer. Categorize and prioritize the feedback."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this feedback: {item}"
                    }
                ]
            )
            return {
                "feedback": item,
                "categories": [c.value for c in result.categories],
                "priority": result.priority,
                "analysis": result.analysis,
                "status": "success"
            }
        except Exception as e:
            attempts += 1
            if attempts > retry_count:
                return {
                    "feedback": item,
                    "error": str(e),
                    "status": "failed"
                }
            await asyncio.sleep(1)  # Backoff before retry

# Batch processor with chunking and progress tracking
async def batch_process(items: List[str],
                        chunk_size: int = 10,
                        concurrency_limit: int = 5,
                        output_file: Optional[str] = None):

    sem = asyncio.Semaphore(concurrency_limit)
    results = []
    processed = 0
    total = len(items)

# Efficiently process data in manageable chunks to prevent memory issues
    for i in range(0, total, chunk_size):
        chunk = items[i:i+chunk_size]

        # Create rate-limited processing function
        async def process_with_sem(item):
            async with sem:
                return await process_item(item)

        # Process current chunk of items
        tasks = [process_with_sem(item) for item in chunk]
        chunk_results = await asyncio.gather(*tasks)
        results.extend(chunk_results)

        # Track and display progress
        processed += len(chunk)
        print(f"Progress: {processed}/{total} ({processed/total*100:.1f}%)")

        # Save intermediate results to prevent data loss
        if output_file:
            with open(output_file, "a") as f:
                for result in chunk_results:
                    f.write(json.dumps(result) + "\n")

    return results

# Example usage
async def main():
    # Test with sample feedback data
    feedback_items = [
        "Your app crashes every time I try to upload a photo. Please fix this ASAP!",
        "I love the new dark mode feature. It makes the app much easier on the eyes.",
        "The checkout process is too complicated. I gave up trying to make a purchase.",
        "Your customer service rep was very helpful in resolving my issue."
        # Examples of different types of feedback
    ]

    results = await batch_process(
        items=feedback_items,
        output_file="feedback_results.jsonl"
    )

# Generate summary statistics from processing results
    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"Successfully processed: {success_count}/{len(results)}")

    # Analyze average priority of feedback items
    priorities = [r.get("priority", 0) for r in results if r["status"] == "success"]
    if priorities:
        print(f"Average priority: {sum(priorities)/len(priorities):.1f}")

    # Generate distribution of feedback categories
    categories = {}
    for r in results:
        if r["status"] == "success":
            for cat in r.get("categories", []):
                categories[cat] = categories.get(cat, 0) + 1

    print("Category distribution:")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    asyncio.run(main())

