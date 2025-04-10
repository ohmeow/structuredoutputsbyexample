# Optional Fields with Literals and Enums
# Demonstrate how to handle optional data in your structured extractions using literals and enums.
# Optional fields can have default values and won't cause extraction failures if the data is missing.

# Import the necessary libraries
from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

# Define an enum for task priority
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Define a model with optional literals and enums
class Task(BaseModel):
    title: str
    description: str
    # Optional enum field with default value
    priority: Optional[Priority] = None
    # Optional literal field with limited values
    status: Optional[Literal["todo", "in-progress", "done"]] = None
    # Optional regular field
    due_date: Optional[str] = None

# Patch the client
client = instructor.from_openai(OpenAI())

# Extract with optional fields
task = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Task,
    messages=[
        {"role": "user", "content": "Create a login page with high priority for the application."}
    ]
)

# Output:
# Task: Create a login page with high priority for the application.
# Description: Create a login page with high priority for the application.
# Priority: high
# Status: None
# Due Date: None
print(f"Task: {task.title}")
print(f"Description: {task.description}")
print(f"Priority: {task.priority}")  # Will be Priority.HIGH enum
print(f"Status: {task.status}")  # Will be None (not specified in text)
print(f"Due Date: {task.due_date or 'Not specified'}")  # Will be None

# Conditional logic with optional enums
if task.priority == Priority.HIGH:
    print("This is a high priority task!")

# Conditional logic with optional literals
if task.status == "in-progress":
    print("This task is currently being worked on.")
elif task.status is None:
    print("This task has no status assigned yet.")