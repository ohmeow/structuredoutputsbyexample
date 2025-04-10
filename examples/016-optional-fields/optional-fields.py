# Optional Fields
# Learn how to handle missing or optional data in your structured extractions with Instructor. This guide covers different approaches to working with optional fields.
# Real-world data is often incomplete, and your models need to gracefully handle missing information.
# Instructor provides multiple ways to work with optional fields, ensuring your data extraction is robust and flexible.

# Import necessary libraries
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional, List
from instructor.dsl.maybe import Maybe

# Patch the client
client = instructor.from_openai(OpenAI())

# Basic optional fields example
class Person(BaseModel):
    name: str
    age: int
    # Optional fields with default value of None
    email: Optional[str] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None

# Extract with optional fields
person = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": "John Smith is 35 years old and works as a software engineer."}
    ]
)

print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Email: {person.email}")  # None
print(f"Phone: {person.phone}")  # None
print(f"Occupation: {person.occupation}")  # "software engineer"

# Optional fields with custom defaults
class Product(BaseModel):
    name: str
    price: float
    # Optional with custom defaults
    currency: str = "USD"
    in_stock: bool = True
    category: Optional[str] = None
    tags: list[str] = Field(default_factory=list)  # Empty list by default

product = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Product,
    messages=[
        {"role": "user", "content": "Our new coffee mug costs 12.99 and is categorized under 'Kitchen'."}
    ]
)

print(f"Product: {product.name}")
print(f"Price: {product.price} {product.currency}")  # USD is the default
print(f"In Stock: {product.in_stock}")  # True is the default
print(f"Category: {product.category}")  # "Kitchen"
print(f"Tags: {product.tags}")  # Empty list by default

# Optional fields with descriptions
class JobApplication(BaseModel):
    name: str = Field(description="Applicant's full name")
    email: str = Field(description="Contact email address")

    # Optional fields with descriptions
    phone: Optional[str] = Field(
        None, description="Phone number in international format (optional)"
    )
    years_experience: Optional[int] = Field(
        None, description="Years of relevant work experience (optional)"
    )
    portfolio_url: Optional[str] = Field(
        None, description="Link to portfolio or personal website (optional)"
    )
    cover_letter: Optional[str] = Field(
        None, description="Brief cover letter or introduction (optional)"
    )

application = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=JobApplication,
    messages=[
        {"role": "user", "content": """
        Job application from Sarah Johnson:
        I'm applying for the software developer position. My email is sarah.j@example.com
        and I have 5 years of experience in frontend development. You can see my work
        at https://sarahjohnson.dev
        """}
    ]
)

print(f"Applicant: {application.name}")
print(f"Email: {application.email}")
print(f"Phone: {application.phone or 'Not provided'}")  # None -> 'Not provided'
print(f"Experience: {application.years_experience or 'Not specified'} years")
print(f"Portfolio: {application.portfolio_url or 'None provided'}")
print(f"Cover Letter: {application.cover_letter or 'Not included'}")

# Using the Maybe type to track presence of fields
class PersonWithMaybe(BaseModel):
    name: str
    age: int
    # Maybe fields track if the information was in the text
    occupation: Maybe[str] = Field(default=None)
    email: Maybe[str] = Field(default=None)
    location: Maybe[str] = Field(default=None)

# Extract with Maybe fields
person_maybe = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=PersonWithMaybe,
    messages=[
        {"role": "user", "content": "John Smith is 35 years old and works as a software engineer."}
    ]
)

print(f"Name: {person_maybe.name}")
print(f"Age: {person_maybe.age}")

# Check if occupation was present
if person_maybe.occupation.exists:
    print(f"Occupation: {person_maybe.occupation.value}")
else:
    print("Occupation: Not mentioned")

# Check if email was present
if person_maybe.email.exists:
    print(f"Email: {person_maybe.email.value}")
else:
    print("Email: Not mentioned")

# Check if location was present
if person_maybe.location.exists:
    print(f"Location: {person_maybe.location.value}")
else:
    print("Location: Not mentioned")

# Optional nested structures
class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: Optional[str] = None

class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None

    # An optional nested object
    address: Optional[Address] = None

class PersonWithNested(BaseModel):
    name: str
    age: int
    contact: Optional[ContactInfo] = None
    hobbies: List[str] = Field(default_factory=list)

person_nested = client.chat.completions.create(
    model="gpt-4",  # Better for complex structures
    response_model=PersonWithNested,
    messages=[
        {"role": "user", "content": """
        Profile: Jane Smith, 42 years old.
        She enjoys hiking, photography, and playing piano.
        Contact her at jane.smith@example.com or at her home in
        123 Maple Street, Toronto, Canada.
        """}
    ]
)

print(f"Name: {person_nested.name}, Age: {person_nested.age}")
print(f"Hobbies: {', '.join(person_nested.hobbies)}")

if person_nested.contact:
    if person_nested.contact.email:
        print(f"Email: {person_nested.contact.email}")
    if person_nested.contact.phone:
        print(f"Phone: {person_nested.contact.phone}")
    if person_nested.contact.address:
        addr = person_nested.contact.address
        print(f"Address: {addr.street}, {addr.city}, {addr.country}")

