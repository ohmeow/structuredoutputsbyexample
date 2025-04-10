# Streaming Lists

# Stream collections of objects one at a time with Instructor.
from pydantic import BaseModel, Field
from typing import List
import instructor
from openai import OpenAI

class Person(BaseModel):
    name: str
    age: int
    occupation: str

# Patch the client
client = instructor.from_openai(OpenAI())

# Create a streaming iterable
people_stream = client.chat.completions.create_iterable(
    model="gpt-3.5-turbo",
    response_model=Person,  # Note: no List[] wrapper needed here
    messages=[
        {"role": "user", "content": """
            Generate profiles for three different people:
            1. A software engineer in their 30s
            2. A teacher in their 40s
            3. A doctor in their 50s
        """}
    ]
)

# Process each person as they are completed
print("Receiving people one at a time:")
for i, person in enumerate(people_stream, 1):
    print(f"\nPerson {i}:")
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")
    print(f"Occupation: {person.occupation}")
    # Note: Each person is fully complete when received

# Example output:# Receiving people one at a time:## Person 1:# Name: Michael Chen# Age: 34# Occupation: software engineer## Person 2:# Name: Sarah Johnson# Age: 42# Occupation: teacher## Person 3:# Name: Robert Garcia# Age: 56# Occupation: doctor

from pydantic import BaseModel, Field
from typing import List, Optional

class Book(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    summary: str = Field(description="Brief summary of the book's plot")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Rating from 0-5 stars")

# Create a streaming iterable for complex objects
books_stream = client.chat.completions.create_iterable(
    model="gpt-3.5-turbo",
    response_model=Book,
    messages=[
        {"role": "system", "content": "Generate detailed book entries with accurate information."},
        {"role": "user", "content": """
            Generate entries for three classic science fiction books.
            Include their titles, authors, publication years, and summaries.
        """}
    ]
)

# Process each book as it's generated
print("Streaming book data:")
for i, book in enumerate(books_stream, 1):
    print(f"\nBook {i}: {book.title} ({book.year})")
    print(f"Author: {book.author}")
    print(f"Genre: {book.genre}")
    print(f"Rating: {book.rating if book.rating is not None else 'Not rated'}")
    print(f"Summary: {book.summary}")

from typing import List, Dict, Any
import time

class Task(BaseModel):
    title: str
    priority: str
    estimated_hours: float
    assigned_to: Optional[str] = None

# Setup for real-time processing
all_tasks = []
total_hours = 0
by_priority = {"high": 0, "medium": 0, "low": 0}
by_assignee = {}

# Create a streaming iterable
tasks_stream = client.chat.completions.create_iterable(
    model="gpt-3.5-turbo",
    response_model=Task,
    messages=[
        {"role": "user", "content": """
            Generate 5 tasks for a software development sprint.
            Include high, medium, and low priority tasks.
            Assign team members: Alex, Jamie, Taylor, and Morgan.
        """}
    ]
)

# Process tasks in real-time
print("Project task planning:")
print("---------------------")

for task in tasks_stream:
    # Update statistics
    all_tasks.append(task)
    total_hours += task.estimated_hours
    by_priority[task.priority.lower()] += 1

    if task.assigned_to:
        by_assignee[task.assigned_to] = by_assignee.get(task.assigned_to, 0) + 1

    # Print the task
    print(f"\nNew Task: {task.title}")
    print(f"Priority: {task.priority}")
    print(f"Estimate: {task.estimated_hours} hours")
    print(f"Assigned to: {task.assigned_to or 'Unassigned'}")

    # Print current statistics
    print("\nCurrent Sprint Stats:")
    print(f"Tasks planned: {len(all_tasks)}")
    print(f"Total hours: {total_hours:.1f}")
    print(f"By priority: {by_priority}")
    print(f"By assignee: {by_assignee}")

    # Simulate a pause for real-time updates
    time.sleep(0.5)

print("\nSprint planning complete!")

from typing import Dict, List, Any, Generator, TypeVar, Generic

T = TypeVar('T')

def combine_streams(streams: Dict[str, Generator[T, None, None]]) -> Generator[Dict[str, T], None, None]:
    """Combine multiple iterables with identification."""
    active_streams = streams.copy()
    results = {key: None for key in streams}

    while active_streams:
        for key, stream in list(active_streams.items()):
            try:
                value = next(stream)
                results[key] = value
                yield results.copy()
            except StopIteration:
                del active_streams[key]

# Create multiple document iterables
class DocumentSummary(BaseModel):
    title: str
    content_type: str
    key_points: List[str]
    word_count: int

# Generate different types of documents
prompts = {
    "emails": "Generate summaries for 3 important emails about project deadlines",
    "reports": "Generate summaries for 2 financial reports about quarterly earnings",
    "articles": "Generate summaries for 2 news articles about technology trends"
}

# Create multiple streams
streams = {}
for category, prompt in prompts.items():
    streams[category] = client.chat.completions.create_iterable(
        model="gpt-3.5-turbo",
        response_model=DocumentSummary,
        messages=[{"role": "user", "content": prompt}]
    )

# Process combined streams as they arrive
for i, result in enumerate(combine_streams(streams), 1):
    print(f"\nUpdate {i}:")
    for category, doc in result.items():
        if doc:
            print(f"  {category.upper()}: {doc.title}")
        else:
            print(f"  {category.upper()}: No documents yet")

from typing import List, Optional, Iterator
import itertools

class NewsHeadline(BaseModel):
    title: str
    source: str
    category: str
    publish_date: str
    summary: str

# Generate a potentially large stream of headlines
headlines_stream = client.chat.completions.create_iterable(
    model="gpt-3.5-turbo",
    response_model=NewsHeadline,
    messages=[
        {"role": "user", "content": "Generate 10 fictional technology news headlines from the past week."}
    ]
)

# Get only the first 3 headlines
print("Top Headlines:")
for i, headline in enumerate(itertools.islice(headlines_stream, 3)):
    print(f"\nHeadline {i+1}: {headline.title}")
    print(f"Source: {headline.source}")
    print(f"Category: {headline.category}")
    print(f"Date: {headline.publish_date}")
    print(f"Summary: {headline.summary}")

# Note: The rest of the stream is not processed, which saves tokens
print("\nShowing only the first 3 headlines.")

