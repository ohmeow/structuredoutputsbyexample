# Field Validation

# 

# Apply validation rules to ensure high-quality data extraction with Instructor.
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

# Define a model with validation rules
class Product(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    price: float = Field(gt=0)  # must be greater than 0
    quantity: int = Field(ge=0)  # must be greater than or equal to 0
    category: str

# Patch the client
client = instructor.from_openai(OpenAI())

# Extract with validation
product = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Product,
    messages=[
        {"role": "user", "content": "We sell a premium coffee mug for $12.99 and have 25 in stock in our kitchen category."}
    ]
)

print(f"Name: {product.name}")
print(f"Price: ${product.price}")
print(f"Quantity: {product.quantity}")
print(f"Category: {product.category}")

from pydantic import BaseModel, Field

class PersonStats(BaseModel):
    name: str
    age: int = Field(ge=0, lt=120)  # 0 ≤ age < 120
    height: float = Field(gt=0, le=300)  # 0 < height ≤ 300 (cm)
    weight: float = Field(gt=0, le=500)  # 0 < weight ≤ 500 (kg)
    body_temperature: float = Field(ge=35, le=42)  # normal human range in Celsius

# Extract with validation
person = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=PersonStats,
    messages=[
        {"role": "user", "content": """
        Patient: John Smith
        Age: 35 years old
        Height: 180 cm
        Weight: 75 kg
        Temperature: 37.2°C
        """}
    ]
)

print(f"Patient: {person.name}")
print(f"Age: {person.age}")
print(f"Height: {person.height} cm")
print(f"Weight: {person.weight} kg")
print(f"Body Temperature: {person.body_temperature}°C")

from pydantic import BaseModel, Field, field_validator
import re

class ContactInfo(BaseModel):
    name: str
    email: str = Field(pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    phone: str = Field(pattern=r'^\+?[1-9]\d{1,14}$')  # E.164 phone format
    website: str = Field(pattern=r'^https?://(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?$')

# Additional custom validation
    @field_validator('name')
    def validate_name(cls, v):
        if len(v.split()) < 2:
            raise ValueError('Name must include at least first and last name')
        return v

# Extract with validation
contact = client.chat.completions.create(
    model="gpt-4",  # More capable for handling pattern constraints
    response_model=ContactInfo,
    messages=[
        {"role": "user", "content": """
        Contact details for our new client:
        Name: John A. Smith
        Email: john.smith@example.com
        Phone: +1-555-123-4567
        Website: https://www.johnsmith.com
        """}
    ]
)

print(f"Name: {contact.name}")
print(f"Email: {contact.email}")
print(f"Phone: {contact.phone}")
print(f"Website: {contact.website}")

# Instructor automatically retries with validation errors:
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int = Field(ge=18, le=100)  # Must be between 18 and 100
    email: str = Field(pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

# This example has invalid data
user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=User,
    max_retries=2,  # Limit retries (default is 3)
    messages=[
        {"role": "user", "content": "Sam is 16 years old and his email is sam@example"}
    ]
)

# Instructor will automatically retry with validation errors to get a fixed response
print(f"Name: {user.name}")
print(f"Age: {user.age}")  # Should be adjusted to valid range
print(f"Email: {user.email}")  # Should include a valid domain

from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

class Reservation(BaseModel):
    guest_name: str
    check_in_date: date
    check_out_date: date
    room_type: str
    num_guests: int = Field(gt=0)
    special_requests: Optional[str] = None

    @field_validator('check_out_date')
    def validate_dates(cls, v, values):
        if 'check_in_date' in values.data and v <= values.data['check_in_date']:
            raise ValueError('check_out_date must be after check_in_date')
        return v

    @field_validator('num_guests')
    def validate_guests(cls, v, values):
        if 'room_type' in values.data:
            if values.data['room_type'].lower() == 'single' and v > 1:
                raise ValueError('Single rooms can only accommodate 1 guest')
            elif values.data['room_type'].lower() == 'double' and v > 2:
                raise ValueError('Double rooms can only accommodate 2 guests')
        return v

# Extract with validation
reservation = client.chat.completions.create(
    model="gpt-4",
    response_model=Reservation,
    messages=[
        {"role": "user", "content": """
        Hotel reservation details:
        Guest: Maria Garcia
        Check-in: 2023-11-15
        Check-out: 2023-11-20
        Room: Double
        Guests: 2
        Special requests: Early check-in if possible
        """}
    ]
)

print(f"Guest: {reservation.guest_name}")
print(f"Stay: {reservation.check_in_date} to {reservation.check_out_date}")
print(f"Room: {reservation.room_type} for {reservation.num_guests} guests")
if reservation.special_requests:
    print(f"Special requests: {reservation.special_requests}")

