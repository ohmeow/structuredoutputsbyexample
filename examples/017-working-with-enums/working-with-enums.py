# Working with Enums

# Use enumerated types with Instructor for consistent, validated extractions. Enums help enforce a fixed set of allowed values.
from enum import Enum
from pydantic import BaseModel
import instructor
from openai import OpenAI

# Define an enum for product categories
class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    BOOKS = "books"
    TOYS = "toys"

class Product(BaseModel):
    name: str
    price: float
    category: ProductCategory

# Patch the client
client = instructor.from_openai(OpenAI())

# Extract with enum validation
product = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Product,
    messages=[
        {"role": "user", "content": "Our new wireless headphones cost $79.99 and belong in our electronics department."}
    ]
)

print(f"Product: {product.name}")
print(f"Price: ${product.price}")
print(f"Category: {product.category}")
# Will be ProductCategory.ELECTRONICS, not just a string

# You can use the enum for comparisons
if product.category == ProductCategory.ELECTRONICS:
    print("This is an electronic product.")

from enum import Enum, auto
from pydantic import BaseModel
from typing import List

# Define priority enum
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Define status enum
class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

class Task(BaseModel):
    title: str
    description: str
    priority: Priority
    status: Status
    tags: List[str] = []

task = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Task,
    messages=[
        {"role": "user", "content": """
        Task Details:
        Title: Fix login page bug
        Description: Users report seeing errors when trying to log in with special characters
        Priority: High
        Status: In Progress
        Tags: bug, authentication, frontend
        """}
    ]
)

print(f"Task: {task.title}")
print(f"Description: {task.description}")
print(f"Priority: {task.priority}")  # Priority.HIGH
print(f"Status: {task.status}")  # Status.IN_PROGRESS
print(f"Tags: {', '.join(task.tags)}")

# Use enums for conditional logic
if task.priority in [Priority.HIGH, Priority.CRITICAL]:
    print("This task requires immediate attention!")

if task.status == Status.IN_PROGRESS:
    print("This task is being worked on.")

from enum import IntEnum
from pydantic import BaseModel

# Define an integer-based enum
class SeverityLevel(IntEnum):
    LOW = 1
    MODERATE = 2
    HIGH = 3
    SEVERE = 4
    CRITICAL = 5

class SecurityIssue(BaseModel):
    title: str
    description: str
    severity: SeverityLevel
    affected_users: int

issue = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=SecurityIssue,
    messages=[
        {"role": "user", "content": """
        Security Alert:
        Issue: Database Exposure
        Details: Customer database was partially exposed due to misconfigured firewall
        Severity: 4 (Severe)
        Affected Users: 5,230
        """}
    ]
)

print(f"Issue: {issue.title}")
print(f"Description: {issue.description}")
print(f"Severity: {issue.severity.name} (Level {issue.severity.value})")  # "SEVERE (Level 4)"
print(f"Affected Users: {issue.affected_users}")

# Use integer enum for thresholds
if issue.severity >= SeverityLevel.HIGH and issue.affected_users > 1000:
    print("This requires executive notification!")

from enum import Enum
from pydantic import BaseModel, Field

class TicketType(str, Enum):
    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"
    DOCUMENTATION = "documentation"
    QUESTION = "question"

class Ticket(BaseModel):
    title: str
    description: str

    # Add descriptions to help the LLM understand the enum
    ticket_type: TicketType = Field(
        description="""Type of ticket with these options:
        - bug: Something is not working correctly
        - feature: A new capability is requested
        - improvement: Enhancement to an existing feature
        - documentation: Updates to documentation
        - question: Question about functionality"""
    )

ticket = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Ticket,
    messages=[
        {"role": "user", "content": """
        New Ticket:
        Title: Add dark mode to application
        Description: Users would like a dark theme option to reduce eye strain when using the app at night
        """}
    ]
)

print(f"Ticket: {ticket.title}")
print(f"Description: {ticket.description}")
print(f"Type: {ticket.ticket_type}")  # Should be TicketType.IMPROVEMENT or TicketType.FEATURE

from enum import Flag, auto
from pydantic import BaseModel, Field

# Define a Flag enum for permissions
class Permissions(Flag):
    NONE = 0
    READ = auto()       # 1
    WRITE = auto()      # 2
    DELETE = auto()     # 4
    ADMIN = auto()      # 8

    # Combinations
    READ_WRITE = READ | WRITE                # 3
    STANDARD = READ | WRITE | DELETE         # 7
    ALL = READ | WRITE | DELETE | ADMIN      # 15

class User(BaseModel):
    name: str
    role: str
    permissions: Permissions = Field(
        description="""User permissions, can be a combination of:
        - READ: Can view content
        - WRITE: Can create and edit content
        - DELETE: Can remove content
        - ADMIN: Has administrative privileges
        - Or predefined combinations like READ_WRITE, STANDARD, or ALL"""
    )

user = client.chat.completions.create(
    model="gpt-4",  # Better for complex models
    response_model=User,
    messages=[
        {"role": "user", "content": """
        User Profile:
        Name: Sarah Johnson
        Role: Content Manager
        Permissions: Can read, write, and delete content
        """}
    ]
)

print(f"User: {user.name}")
print(f"Role: {user.role}")
print(f"Permissions: {user.permissions.name}")  # Should be "STANDARD"

# Check individual permissions
if Permissions.READ in user.permissions:
    print("User can read content")

if Permissions.WRITE in user.permissions:
    print("User can write content")

if Permissions.ADMIN in user.permissions:
    print("User has admin privileges")
else:
    print("User does not have admin privileges")

