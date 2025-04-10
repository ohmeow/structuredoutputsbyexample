# Partial Extraction with Instructor
# This example demonstrates how to handle partial data extraction when complete information isn't available.
# In real-world scenarios, documents may contain incomplete information, requiring graceful handling of missing data.
# Partial extraction allows you to extract as much structured data as possible while clearly marking what's missing.

# Import necessary libraries
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional

# Initialize the OpenAI client with instructor
client = instructor.from_openai(OpenAI())

# Define a model that allows for partial extraction with Optional fields
class UserProfile(BaseModel):
    """User profile with optional fields for partial extraction."""
    name: str = Field(description="Full name of the user")
    email: Optional[str] = Field(description="User's email address", default=None)
    age: Optional[int] = Field(description="User's age in years", default=None)
    occupation: Optional[str] = Field(description="User's job or profession", default=None)
    bio: Optional[str] = Field(description="Short user biography", default=None)

# Example 1: Complete profile extraction
complete_profile = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract user info: John Smith, john.smith@example.com, 35 years old, Software Engineer, Passionate about coding and hiking."
        }
    ],
    response_model=UserProfile
)

print("Complete Profile:")
print(complete_profile.model_dump_json(indent=2))

# Example 2: Partial profile extraction with missing fields
partial_profile = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Extract user info: Jane Doe, Marketing Specialist"
        }
    ],
    response_model=UserProfile
)

print("\nPartial Profile:")
print(partial_profile.model_dump_json(indent=2))

# Define a more complex model with nested optional components
class Address(BaseModel):
    """Address information with optional components."""
    street: Optional[str] = Field(description="Street address", default=None)
    city: str = Field(description="City name")
    state: Optional[str] = Field(description="State or province", default=None)
    zip_code: Optional[str] = Field(description="Postal code", default=None)
    country: str = Field(description="Country name")

class ContactInfo(BaseModel):
    """Contact information with optional components."""
    email: Optional[str] = Field(description="Email address", default=None)
    phone: Optional[str] = Field(description="Phone number", default=None)
    address: Optional[Address] = Field(description="Physical address", default=None)

class Customer(BaseModel):
    """Customer profile with deeply nested optional fields."""
    name: str = Field(description="Customer's full name")
    id: Optional[str] = Field(description="Customer ID", default=None)
    contact: ContactInfo = Field(description="Contact information")
    preferences: Optional[dict] = Field(description="Customer preferences", default=None)

# Example 3: Complex partial extraction with nested fields
customer = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": "Customer: Michael Johnson, ID: MJ-123, Email: michael@example.com, Lives in San Francisco, USA"
        }
    ],
    response_model=Customer
)

print("\nComplex Partial Extraction:")
print(customer.model_dump_json(indent=2))

# Example 4: Providing validation guidance for partial extraction
class Product(BaseModel):
    """Product information with validation hints."""
    name: str = Field(description="Product name")
    price: Optional[float] = Field(
        description="Product price in USD (leave empty if unknown, never guess)",
        default=None
    )
    category: Optional[str] = Field(
        description="Product category (leave empty if unspecified, do not infer)",
        default=None
    )
    description: Optional[str] = Field(
        description="Product description (if available)",
        default=None
    )

# Example with instructions for handling missing data
product = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user", 
            "content": "Product: Wireless Headphones, $79.99"
        }
    ],
    response_model=Product
)

print("\nPartial Extraction with Validation Guidance:")
print(product.model_dump_json(indent=2))

# Best practices summary
print("\nPartial Extraction Best Practices:")
print("1. Use Optional types for fields that might be missing")
print("2. Provide default values (typically None) for optional fields")
print("3. Include clear descriptions for fields with instructions on handling missing data")
print("4. For complex extractions, use nested models with optional components")
print("5. Be explicit about when to extract vs. when to leave fields empty")
print("6. Process extracted data with awareness of potential missing values") 