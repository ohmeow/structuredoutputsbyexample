# Type Adapters
# Learn how to leverage Pydantic Type Adapters with Instructor for advanced validation and data conversion. This guide covers complex data structures, error handling, and custom type validation.
# When working with complex or nested data structures, standard validation approaches can become cumbersome and error-prone.
# Type Adapters provide a powerful way to validate, convert and process structured data with better error messages and flexible validation rules.

# Import necessary libraries
import json
from typing import List, Dict, Any, Optional, Union
from pydantic import TypeAdapter, BaseModel, Field
import instructor
from openai import OpenAI

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Example 1: Basic Type Adapter for Lists
print("\n=== Example 1: Type Adapter for Lists ===")

# Define a model for validation
class User(BaseModel):
    name: str
    age: int
    skills: List[str]

# Create a type adapter for a list of users
UserListAdapter = TypeAdapter(List[User])

# Define an extraction function
def extract_users_from_text(text: str) -> List[User]:
    """Extract a list of users from text and validate with Type Adapter."""
    # Get raw JSON data from LLM
    raw_data = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Extract all users from this text as a JSON array with key 'users': {text}"
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    ).choices[0].message.content

    # Parse JSON
    try:
        data = json.loads(raw_data)
        # Use type adapter for validation
        users = UserListAdapter.validate_python(data.get("users", []))
        return users
    except Exception as e:
        print(f"Error parsing data: {e}")
        return []

# Example usage
text = """
Team members:
- John Smith, 32 years old, skills: Python, JavaScript, Docker
- Maria Garcia, 28 years old, skills: UX Design, Figma, HTML/CSS
- Alex Johnson, 35 years old, skills: Project Management, Agile, Scrum
"""

users = extract_users_from_text(text)
for user in users:
    print(f"{user.name} ({user.age}): {', '.join(user.skills)}")

# Example 2: Type Adapters with Nested Structures
print("\n=== Example 2: Type Adapters with Nested Structures ===")

# Define some models
class Comment(BaseModel):
    user: str
    text: str
    timestamp: str

class Post(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]
    comments: List[Comment]

# Create type adapters
CommentAdapter = TypeAdapter(Comment)
PostAdapter = TypeAdapter(Post)
PostDictAdapter = TypeAdapter(Dict[str, Post])

# Process raw data with type adapters
def process_comment(raw_comment: Dict[str, Any]) -> Comment:
    """Validate and convert a raw comment dict to a Comment model."""
    return CommentAdapter.validate_python(raw_comment)

def process_post(raw_post: Dict[str, Any]) -> Post:
    """Validate and convert a raw post dict to a Post model."""
    return PostAdapter.validate_python(raw_post)

def process_posts_dict(raw_posts: Dict[str, Any]) -> Dict[str, Post]:
    """Validate and convert a dictionary of posts."""
    return PostDictAdapter.validate_python(raw_posts)

# Example data
raw_comment = {
    "user": "alice",
    "text": "Great post!",
    "timestamp": "2023-06-15T14:30:00Z"
}

raw_post = {
    "id": 1,
    "title": "Introduction to Type Adapters",
    "content": "Type adapters are a powerful feature...",
    "tags": ["pydantic", "python", "validation"],
    "comments": [
        raw_comment,
        {"user": "bob", "text": "Thanks for sharing!", "timestamp": "2023-06-15T15:45:00Z"}
    ]
}

# Validate and convert the data
comment = process_comment(raw_comment)
post = process_post(raw_post)

print(f"Comment by {comment.user}: {comment.text}")
print(f"Post: {post.title} with {len(post.comments)} comments and tags: {', '.join(post.tags)}")

# Example 3: Type Adapters for Complex API Responses
print("\n=== Example 3: Type Adapters for Complex API Responses ===")

# Define complex nested structures
class Address(BaseModel):
    street: str
    city: str
    postal_code: str
    country: str

class ContactInfo(BaseModel):
    email: str
    phone: Optional[str] = None
    address: Address

class Customer(BaseModel):
    id: str
    name: str
    contact_info: ContactInfo
    account_type: str
    active: bool

# Create nested type adapters
AddressAdapter = TypeAdapter(Address)
ContactInfoAdapter = TypeAdapter(ContactInfo)
CustomerAdapter = TypeAdapter(Customer)
CustomerListAdapter = TypeAdapter(List[Customer])

# Process data with validation
def process_customers(data: Dict[str, Any]) -> List[Customer]:
    """Extract and validate customer data from a complex API response."""
    try:
        # Extract customer data from a complex API response
        customers_data = data.get("results", {}).get("customers", [])
        return CustomerListAdapter.validate_python(customers_data)
    except Exception as e:
        print(f"Validation error: {e}")
        return []

# Example API response data
api_response = {
    "status": "success",
    "results": {
        "customers": [
            {
                "id": "cust-001",
                "name": "Acme Corporation",
                "contact_info": {
                    "email": "contact@acme.com",
                    "phone": "555-123-4567",
                    "address": {
                        "street": "123 Main St",
                        "city": "San Francisco",
                        "postal_code": "94105",
                        "country": "USA"
                    }
                },
                "account_type": "enterprise",
                "active": True
            },
            {
                "id": "cust-002",
                "name": "Globex Inc",
                "contact_info": {
                    "email": "info@globex.com",
                    "address": {
                        "street": "456 Market St",
                        "city": "New York",
                        "postal_code": "10001",
                        "country": "USA"
                    }
                },
                "account_type": "small_business",
                "active": True
            }
        ]
    }
}

# Process and validate the data
customers = process_customers(api_response)
print(f"Processed {len(customers)} valid customers")
for customer in customers:
    print(f"- {customer.name} ({customer.id})")
    print(f"  Email: {customer.contact_info.email}")
    print(f"  Address: {customer.contact_info.address.city}, {customer.contact_info.address.country}")

# Benefits and Use Cases for Type Adapters
print("\n=== Benefits of Type Adapters ===")
print("1. Reusable Validation Logic: Create adapters once and reuse them throughout your codebase")
print("2. Better Error Messages: Get detailed validation errors for complex structures")
print("3. Flexible Data Sources: Process data from LLMs, APIs, databases with the same validation")
print("4. Type Safety: Ensure type correctness in your Python code")
print("5. Complex Validation: Handle deeply nested structures with elegant validation logic")
print("6. Composition: Combine adapters to handle even more complex data structures")
print("7. Performance: Validate large collections of objects efficiently")

